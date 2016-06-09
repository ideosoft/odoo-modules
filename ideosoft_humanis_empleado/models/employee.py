#-*- coding:utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime
from openerp.exceptions import except_orm, Warning, RedirectWarning

import logging
_logger = logging.getLogger(__name__)

def preposicion(string):
    preposiciones = [ (' De ', ' de '), (' Y ', ' y '), (' En ', ' en ')]
    
    for k, v in preposiciones:
        string = string.replace(k, v)
    return string

class Employee(models.Model):

    _name = 'hr.employee'
    _inherit = 'hr.employee'
    
    @api.model
    def create(self, values):
        complete_name = ""
    
        if values['nombre']:
            values['nombre'] = preposicion(values['nombre'].title())
            complete_name += values['nombre']

        if values['apellido1']:
            values['apellido1'] = preposicion(values['apellido1'].title())
            complete_name += " " + values['apellido1']

        if values['apellido2']:
            values['apellido2'] = preposicion(values['apellido2'].title())
            complete_name += " " + values['apellido2']

        values['name'] = complete_name
        
        id = super(Employee, self).create(values)
        return id


    @api.one
    @api.onchange('nombre')
    def check_nombre(self):
        if self.nombre:
            self.nombre = preposicion(self.nombre.title())
            
    @api.one
    @api.onchange('apellido1')
    def check_apellido1(self):
        if self.apellido1:
            self.apellido1 = preposicion(self.apellido1.title())
          
    @api.one
    @api.onchange('apellido2')
    def check_apellido2(self):
        if self.apellido2:
            self.apellido2 = preposicion(self.apellido2.title())
            
    @api.onchange('nombre', 'apellido1', 'apellido2')
    def check_change(self):
        complete_name = None
        if self.nombre:
            complete_name = self.nombre
        if self.apellido1:
            complete_name += " " + self.apellido1
        if self.apellido2:
            complete_name += " " + self.apellido2

        if complete_name:
            self.name = self.name_related = preposicion(complete_name.title())
        
    @api.one
    @api.depends('birthday')
    def _compute_age(self):
        if self.birthday:
            age = int((datetime.now()-datetime.strptime(self.birthday,"%Y-%m-%d")).days/365.25)
            if age < 0:
                age = 0
            self.edad = age
        else:
            self.edad = 0
            
    @api.one
    def sumaturno(self):
        max = self.num_max_turnos
        if self.num_turnos < max:
            self.num_turnos += 1
        else: 
            raise Warning('Número de turnos permitidos al mes alcanzado')
            
    @api.one
    def restaturno(self):
        if self.num_turnos > 0:
            self.num_turnos -= 1
        else: 
            return False
            
            
    @api.one
    @api.onchange('minusvalia')
    def check_minusvalia(self):
        if not self.minusvalia:
            self.cant_minusvalia = 0
    
    
    @api.one
    def setActivo(self):
        self.estado = 'act'
    
    @api.one
    def setExcedencia(self):
        self.estado = 'exc'
    
    @api.one
    def setBaja(self):
        self.estado = 'baj'
        
    @api.one
    def setFinCamp(self):
        self.estado = 'fin'

    
    @api.one
    @api.onchange('nif')
    def _validate_NIF(self):
        if self.nif:
            # self.nif = self.nif.upper()
            nif = self.nif
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X':'0', 'Y':'1', 'Z':'2'}
            numeros = "1234567890"
            if len(nif) == 9:
                dig_control = nif[8]
                nif = nif[:8]
                self.tipo_nif = "NIF"
                if nif[0] in dig_ext:
                    self.tipo_nif = "NIE"
                    nif = nif.replace(nif[0], reemp_dig_ext[nif[0]])
                return len(nif) == len([n for n in nif if n in numeros]) \
                and tabla[int(nif)%23] == dig_control
            return False
                
                
    def _calculate_age(self):
        res = {}
        if self.birthday:
            age = int((datetime.now()-datetime.strptime(self.birthday,"%Y-%m-%d")).days/365.25)
            if age < 0:
                age = 0
            res = age
        return res
                
    def _search_age(self, operator, value):
        ids = []
        for record in self.search([]):
            if record.birthday:
                age = record._calculate_age()
                if operator == '=':
                    if age == value:
                        ids.append(record.id)
                if operator == '!=':
                    if age != value:
                        ids.append(record.id)
                if operator == '<':
                    if age < value:
                        ids.append(record.id)
                if operator == '>':
                    if age > value:
                        ids.append(record.id)
                if operator == '>=':
                    if age >= value:
                        ids.append(record.id)
                if operator == '<=':
                    if age <= value:
                        ids.append(record.id)
        return [('id','=',ids)]

        
    @api.one
    @api.onchange('better_zip_id')
    def on_change_zip_id(self):
        if self.better_zip_id:
            self.zip = self.better_zip_id.name
            #self.city = self.better_zip_id.city
            self.state_id = self.better_zip_id.state_id
            self.country_id = self.better_zip_id.country_id
            
        
    @api.one     
    @api.onchange('company_id')
    def on_change_company(self):
        self.area_id = ''
        self.servicio_id = ''
    
    
    @api.one
    @api.onchange('area_id')
    def on_change_area(self):
        self.servicio_id = ''


    @api.one
    def _show_center(self):
        
        contract_ids = self.env['hr.contract'].search([('employee_id','=',self.id)])
        
        for contract_id in contract_ids:
            contract = self.env['hr.contract'].browse(contract_id.ids)
            
            if not contract.date_end or (contract.date_end and datetime.strptime(contract.date_end,"%Y-%m-%d") > datetime.now()):
                centro = self.env['res.company.area.servicio.centrotrabajo'].browse(contract.centrotrabajo_id.ids)
                self.centrotrabajo = centro.name
            
            
    @api.one
    def _compute_convenio_days(self):
        if self.convenio_id:
            convenio = self.env['hr.employee.convenio'].browse(self.convenio_id.id)
            self.convenio_days = convenio.vacation_days
            
    @api.one
    def _compute_personal_days(self):
        if self.convenio_id:
            convenio = self.env['hr.employee.convenio'].browse(self.convenio_id.id)
            self.personal_days = convenio.personal_days
	
    
    @api.one
    def _compute_annual_days(self):
    
        contracts = self.env['hr.contract'].search([('employee_id','=',self.id)])
        convenio = self.env['hr.employee.convenio'].browse(self.convenio_id.id)
        
        for contract in contracts:
        
            # no computo las prorrogas como contratos normales
            if not contract.es_prorroga:

                # si no tiene fecha fin de contrato es el contrato en vigor
                if not contract.date_end:
                
                    # calculo la cantidad de días entre la fecha inicio de contrato y el final de año
                    next_year = datetime.strptime(str(date.today().year + 1) + "-01-01","%Y-%m-%d")
                    
                    # la fecha de inicio pertenece al año actual
                    if datetime.strptime(contract.date_start,"%Y-%m-%d").year == date.today().year:
                        delta = next_year - datetime.strptime(contract.date_start,"%Y-%m-%d")
                        self.annual_days = delta.days * convenio.vacation_days / 365
                        
                    # la fecha de inicio NO pertenece al año actual                
                    else:
                        self.annual_days = convenio.vacation_days
                        
                # si tiene fecha fin y es mayor que la fecha actual es el contrato en vigor
                elif (datetime.strptime(contract.date_end,"%Y-%m-%d") > datetime.now() or (contract.date_end_prorroga and datetime.strptime(contract.date_end_prorroga,"%Y-%m-%d") > datetime.now())):
                
                    # compruebo si tiene prorrogas, y si es asi establezco la fecha fin de contrato a la de la prorroga
                    if contract.date_end_prorroga:
                        contract.date_end = contract.date_end_prorroga
                        
                    # si la fecha fin pertenece a un año superior al actual
                    if datetime.strptime(contract.date_end,"%Y-%m-%d").year > date.today().year:
                        next_year = datetime.strptime(str(date.today().year + 1) + "-01-01","%Y-%m-%d")
                        
                        # la fecha de inicio pertenece al año actual
                        if datetime.strptime(contract.date_start,"%Y-%m-%d").year == date.today().year:
                            delta = next_year - datetime.strptime(contract.date_start,"%Y-%m-%d")
                            self.annual_days = delta.days * convenio.vacation_days / 365
                            
                        # la fecha de inicio NO pertenece al año actual                
                        else:
                            self.annual_days = convenio.vacation_days
                            
                    # si la fecha fin pertenece al año actual                
                    else:
                        # la fecha de inicio pertenece al año actual
                        if datetime.strptime(contract.date_start,"%Y-%m-%d").year == date.today().year:
                            delta = datetime.strptime(contract.date_end,"%Y-%m-%d") - datetime.strptime(contract.date_start,"%Y-%m-%d")
                            self.annual_days = delta.days * convenio.vacation_days / 365
                            
                        # la fecha de inicio NO pertenece al año actual
                        else:
                            delta = datetime.strptime(contract.date_end,"%Y-%m-%d") - datetime.strptime(str(date.today().year) + "-01-01","%Y-%m-%d")
                            self.annual_days = delta.days * convenio.vacation_days / 365

           
        
    def get_requested_days(self, contract_id):
        count = 0
        days = self.env['hr.employee.vacations'].search([('contract_id','=',contract_id)])
        if days:
            for d in days:
                count = count + float(d.type)
                
        return count
        
        

    @api.one
    def _compute_requested_days(self):
        contracts = self.env['hr.contract'].search([('employee_id','=',self.id)])
        for contract in contracts:  
            # no computo las prorrogas como contratos normales
            if not contract.es_prorroga:
                # si no tiene fecha fin de contrato o si es mayor que hoy es el contrato en vigor
                if not contract.date_end or (contract.date_end and datetime.strptime(contract.date_end,"%Y-%m-%d") > datetime.now()) or (contract.date_end_prorroga and datetime.strptime(contract.date_end_prorroga,"%Y-%m-%d") > datetime.now()):
                    self.requested_days = self.get_requested_days(contract.id)
                    
                    

    @api.one
    def _compute_hanging_days(self):
    
        contracts = self.env['hr.contract'].search([('employee_id','=',self.id)])
        convenio = self.env['hr.employee.convenio'].browse(self.convenio_id.id)
        
        for contract in contracts:

            # no computo las prorrogas como contratos normales
            if not contract.es_prorroga:
        
                # si no tiene fecha fin de contrato es el contrato en vigor
                if not contract.date_end:
                
                    # calculo los dias solicitados para este contrato
                    requested_days = self.get_requested_days(contract.id)
                
                    # calculo la cantidad de días entre la fecha inicio de contrato y el final de año
                    next_year = datetime.strptime(str(date.today().year + 1) + "-01-01","%Y-%m-%d")
                    
                    # si la fecha de inicio pertenece al año actual
                    if datetime.strptime(contract.date_start,"%Y-%m-%d").year == date.today().year:

                        delta = next_year - datetime.strptime(contract.date_start,"%Y-%m-%d")

                        hanging_days = float(delta.days * convenio.vacation_days / 365 - requested_days + self.previous_year_days)
                        
                        if hanging_days < 0:
                            self.hanging_days = 0
                            return
                        else:
                            self.hanging_days = hanging_days                            
                            return
                    
                    # si la fecha de inicio NO pertenece al año actual                
                    else:
                        hanging_days = convenio.vacation_days - requested_days + self.previous_year_days
                        if hanging_days < 0:
                            self.hanging_days = 0
                            return
                        else:
                            self.hanging_days = hanging_days
                            return
                        

                # si tiene fecha fin y es mayor que la fecha actual es el contrato en vigor
                elif datetime.strptime(contract.date_end,"%Y-%m-%d") > datetime.now():
                    
                    # calculo los dias solicitados para este contrato
                    requested_days = self.get_requested_days(contract.id)
                    
                    # compruebo si tiene prorrogas, y si es asi establezco la fecha fin de contrato a la de la prorroga
                    if contract.date_end_prorroga:
                        contract.date_end = contract.date_end_prorroga                    
                    
                    # si la fecha fin pertenece a un año superior al actual
                    if datetime.strptime(contract.date_end,"%Y-%m-%d").year > date.today().year:
                        
                        next_year = datetime.strptime(str(date.today().year + 1) + "-01-01","%Y-%m-%d")
                        
                        # la fecha de inicio pertenece al año actual
                        if datetime.strptime(contract.date_start,"%Y-%m-%d").year == date.today().year:

                            delta = next_year - datetime.strptime(contract.date_start,"%Y-%m-%d")
                            
                            hanging_days = float(delta.days * convenio.vacation_days / 365 - requested_days + self.previous_year_days)
                            
                            if hanging_days < 0:
                                self.hanging_days = 0
                                return
                            else:
                                self.hanging_days = hanging_days
                                return
                                
                        # la fecha de inicio NO pertenece al año actual             
                        else:
                            hanging_days = convenio.vacation_days - requested_days + self.previous_year_days
                            if hanging_days < 0:
                                self.hanging_days = 0
                                return
                            else:
                                self.hanging_days = hanging_days   
                                return
                                
                    # si la fecha fin pertenece al año actual                
                    else:
                    
                        # la fecha de inicio pertenece al año actual
                        if datetime.strptime(contract.date_start,"%Y-%m-%d").year == date.today().year:

                            delta = datetime.strptime(contract.date_end,"%Y-%m-%d") - datetime.strptime(contract.date_start,"%Y-%m-%d")
           
                            hanging_days = float(delta.days * convenio.vacation_days / 365 - requested_days + self.previous_year_days)
                            
                            if hanging_days < 0:
                                self.hanging_days = 0
                                return
                            else:
                                self.hanging_days = hanging_days
                                return
           
                        # la fecha de inicio NO pertenece al año actual
                        else:
                        
                            delta = datetime.strptime(contract.date_end,"%Y-%m-%d") - datetime.strptime(str(date.today().year) + "-01-01","%Y-%m-%d")

                            hanging_days = float(delta.days * convenio.vacation_days / 365 - requested_days + self.previous_year_days)
                            if hanging_days < 0:
                                self.hanging_days = 0
                                return
                            else:
                                self.hanging_days = hanging_days
                                return
                                
                  
    
    @api.multi
    def open_vacation_view(self):
     
        vacations = self.env['hr.employee.vacations'].search([('employee_id','=',self.id)])
        if(vacations):
            
            days = []
            for day in vacations:
                days.append(day.date)
                
            date_start = min(days)
            date_stop = max(days)
            
            _logger.warning("DATE START: %s", date_start)
            _logger.warning("DATE STOP: %s", date_stop)

            return {
                "type": "ir.actions.act_window",
                "res_model": "hr.employee.vacations",
                "views": [[False, "tree"], [False, "form"]],
                "domain": [["employee_id", "=", self.id]],
                "target": "new",
                "context": {    
                                'employee_id': self.id,
                                'date_start': date_start,
                                'date_stop': date_stop
                            }
            }
        else: 
            raise Warning("No existen vacaciones para este empleado")
    
       
       
    # CAMPOS
    company_id = fields.Many2one(comodel_name='res.company', string='Empresa', ondelete='set null')
    area_id    = fields.Many2one(comodel_name='res.company.area', string='Area', ondelete='set null')
    
    servicio_id = fields.Many2one(comodel_name='res.company.area.servicio', string='Servicio', ondelete='set null')
    centrotrabajo = fields.Char(string='Centro Trabajo', compute=_show_center)
    
    nombre = fields.Char(string="Nombre")
    apellido1 = fields.Char(string="1er Apellido")
    apellido2 = fields.Char(string="2do Apellido")
    
    nif = fields.Char(string="NIF", size=9)
    tipo_nif = fields.Char(string="TIPO NIF", default="") # compute=_compute_nif_type
    nie_exp = fields.Date(string="Expiración NIE")
    nss = fields.Char(string="N. Seguridad Social")
    edad = fields.Integer(string="Edad", compute=_compute_age, default=0, search="_search_age")
    minusvalia = fields.Boolean(string="Minusvalía")
    cant_minusvalia = fields.Integer(string="Cantidad minusvalía")
    
    telefono_personal = fields.Char(string="Telefono")
    email_personal = fields.Char(string="Email")
    
    business_phone = fields.Many2one(comodel_name='hr.employee.phone', string='Tlfno empresa')
    
    phone_extension = fields.Char(string="Extension", required=False)
    domain_user = fields.Char(string="Usuario Dominio", required=False)
    
    salario = fields.Float(string="Salario", required=False)
    
    ccc = fields.Char(string="Cuenta bancaria", size=20)
    
    # VACACIONES
    previous_year_days = fields.Float(string="Días años anteriores", digits=(10,2), default=0)
    requested_days = fields.Float(string="Días solicitados", digits=(10, 2), compute=_compute_requested_days)
    hanging_days = fields.Float(string="Días restantes", digits=(10, 2), compute=_compute_hanging_days)
    convenio_days = fields.Integer(string="Días anuales por convenio", compute=_compute_convenio_days)
    personal_days = fields.Integer(string="Días asuntos propios", compute=_compute_personal_days)
    annual_days = fields.Integer(string="Días correspondientes año actual", compute=_compute_annual_days)
    vacation_notes = fields.Text(string="Observaciones")
    
    # INTERNACIONALIZACION
    better_zip_id = fields.Many2one(
        'res.better.zip',
        string='Location',
        select=1,
        help='Usa la ciudad o el CP para buscar la dirección',
    )
    
    street = fields.Char(string="Dirección")
    zip = fields.Char(string="Cód. Postal", size=5)
    city = fields.Char(string="Municipio")
    state_id = fields.Many2one('res.country.state', string="Provincia")
    country_id = fields.Many2one('res.country', string="País")
    nationality_id = fields.Many2one('res.country', string="Nacionalidad")
    
    notas = fields.Text(string="Notas")
    notas_privadas = fields.Text(string="Notas Privadas")
    
    estado = fields.Selection([
            ('act','Activo'),
            ('exc','Excedencia'),
            ('baj','Baja'),
            ('fin','Fin de campaña')
        ], string='Estado', select=True, index=True, copy=False)
        
        
    # RELACIONES
    absentismo_ids = fields.One2many(comodel_name='hr.employee.absentismo', inverse_name='employee_id', string='Absentismo')
    cita_ids = fields.One2many(comodel_name='hr.employee.cita', inverse_name='employee_id', string='Citas')
    convenio_id = fields.Many2one('hr.employee.convenio', string="Convenio", ondelete='set null')
    curso_ids = fields.One2many(comodel_name='hr.employee.cursoempleado', inverse_name='employee_id', string='Cursos')
    embargo_ids = fields.One2many(comodel_name='hr.employee.embargo', inverse_name='employee_id', string='Embargos')
    experience_ids = fields.One2many(comodel_name='hr.employee.experience', inverse_name='employee_id', string='Experiencia')
    family_ids = fields.One2many(comodel_name='hr.employee.family', inverse_name='employee_id', string='Familiar')
    observacion_ids = fields.One2many(comodel_name='hr.employee.observacion', inverse_name='employee_id', string='Observaciones')
    puesto_ids = fields.One2many(comodel_name='hr.employee.puesto', inverse_name='employee_id', string='Puestos')
    recurso_ids = fields.One2many(comodel_name='hr.employee.recurso', inverse_name='employee_id', string='Recursos')
    #sancion_ids = fields.One2many(comodel_name='hr.employee.sancion', inverse_name='employee_id', string='Sanciones')
    sindicato_id = fields.Many2one('hr.employee.sindicato', string='Sindicato', ondelete='set null')
    solicitud_ids = fields.One2many(comodel_name='hr.employee.solicitud', inverse_name='employee_id', string='Solicitudes')
    sueldo_ids = fields.One2many(comodel_name='hr.employee.sueldo', inverse_name='employee_id', string='Sueldo')
    vacations_ids = fields.One2many(comodel_name='hr.employee.vacations', inverse_name='employee_id', string='Vacaciones')
    
    
    _sql_constraints = [
        ('nif_unico', 'unique(nif)', 'Ya existe ese NIF/NIE en la base de datos')
    ]