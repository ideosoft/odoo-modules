# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime
import pprint
import time
from dateutil import rrule

class Convenio(models.Model):

    _name = 'hr.employee.convenio'
    _description = "Convenio"

    code = fields.Char(string="Código")
    date_start = fields.Date(string="Fecha inicio")
    date_end = fields.Date(string="Fecha fin")
    description = fields.Text(string="Descripción")
    vacation_days = fields.Integer(string="Días de vacaciones")
    personal_days = fields.Integer(string="Días de asuntos propios")
    

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.description: 
                result.append((record.id, "%s - %s" % (record.code, record.description)))
            else: 
                result.append((record.id, "%s" % (record.code)))
        return result

WEEKDAYS = [
    'Lunes',
    'Martes',
    'Miércoles',
    'Jueves',
    'Viernes',
    'Sábado',
    'Domingo',
]
    
class PublicHoliday(models.Model):
    
    _name = 'res.public_holiday'
    _description = "Festivo"
    _order = 'date'
    
    @api.one
    @api.depends('date')
    def _compute_weekday(self):
        if self.date:
            weekday = datetime.strptime(self.date,"%Y-%m-%d").weekday()
            self.weekday = WEEKDAYS[weekday]

    @api.one
    @api.depends('date')
    def _compute_year(self):
        if self.date:
            year = datetime.strptime(self.date,"%Y-%m-%d").year
            self.year = "%d" % year
            
    date = fields.Date(string="Fecha", required=True)
    name = fields.Char(string="Nombre", required=True)
    type = fields.Char(string="",default=0)
    weekday = fields.Char(string="Día de la Semana", compute=_compute_weekday)
    year = fields.Char(string="Año", compute=_compute_year)
    
    
class FestivoConvenio(models.Model):

    _name = 'hr.employee.festivoconvenio'
    _inherit = 'res.public_holiday'
    _description = "Festivo de convenio"
    _order = 'date'
    
    convenio_id = fields.Many2one('hr.employee.convenio', string="Convenio", ondelete='cascade', required=True)
    
    
    
class FestivoWizard(models.TransientModel):

    _name = 'hr.employee.festivoconveniowizard'
    _description = 'Wizard'

    convenio_id = fields.Integer(string="Convenio id")
    allow_generals = fields.Boolean(string="Habilitar festivos generales")
    aux_dates = fields.Char(string="Dias festivos de convenio")
    
    @api.one
    @api.depends('convenio_id','aux_dates')
    def setFestivosConvenio(self):

        if self.convenio_id:

            actual_fests = self.env['hr.employee.festivoconvenio'].search([('convenio_id','=',self.convenio_id)])
            
            for f in actual_fests:
                f.unlink()
            
            convenio = self.env['hr.employee.convenio'].browse(self.convenio_id)
            name = convenio.code
            
            if self.aux_dates:

                for fest in self.aux_dates.split(','):
                    date = datetime.strptime(fest,"%d/%m/%Y")
                        
                    festivo = self.env['hr.employee.festivoconvenio'].create({
                        'name': name,
                        'date': date,
                        'convenio_id': self.convenio_id
                    })

        else:
            raise Warning("No se ha podido guardar los festivos del convenio. No se ha obtenido ningún convenio válido.")
        
        
    
class TipoAbsentismo(models.Model):
    
    _name = "hr.employee.tipoabsentismo"
    _description = "Tipo de absentismo"
        
    code = fields.Char(string="Código")
    name = fields.Char(string="Tipo de absentismo")


class Absentismo(models.Model):

    _name="hr.employee.absentismo"
    _description="Absentismo"
    
    
    @api.one
    @api.onchange('fecha_abs')
    def fill_dates(self):
        if self.fecha_abs:
            self.fecha_baja = self.fecha_abs
            self.fecha_alta = self.fecha_abs
            
    @api.one
    @api.onchange('fecha_alta')
    def get_dias_baja(self):
        if self.fecha_baja and self.fecha_alta:
            f_baja = datetime.strptime(self.fecha_baja, "%Y-%m-%d")
            f_alta = datetime.strptime(self.fecha_alta, "%Y-%m-%d")
            # CALCULO DE DIAS CONTANDO FINES DE SEMANA
            #self.dias_baja = abs((f_alta - f_baja).days)
            # CALCULO DE DIAS SIN CONTAR FINES DE SEMANA
            self.dias_baja = self.calculate_working_days(f_baja, f_alta)

    def calculate_working_days(self, date_start_obj, date_end_obj):
        weekdays = rrule.rrule(rrule.DAILY, byweekday=range(0, 5), dtstart=date_start_obj, until=date_end_obj)
        weekdays = len(list(weekdays))
        #if int(time.strftime('%H')) >= 18:
        #    weekdays -= 1
        return weekdays
        
        
    # @api.multi
    # def printAbsentismo(self):
        
        # if not self.fecha_baja: 
            # raise Warning('No se ha introducido ninguna fecha de baja.')
    
        # return self.env['report'].get_action(self, 'ideosoft_humanis_convenio.report_absentismo')
                
            
            

    employee_id = fields.Many2one('hr.employee', string='Empleado', ondelete='cascade')
    fecha_abs = fields.Date(string="Fecha de absentismo")
    tipo_absent_id = fields.Many2one('hr.employee.tipoabsentismo', ondelete='set null', string="Tipo", required=True)
    fecha_baja = fields.Date(string="Fecha de baja")
    fecha_alta = fields.Date(string="Fecha de alta")
    dias_baja = fields.Integer(string="Días de baja", readonly=True)
    descripcion = fields.Text(string="Descripción")
    reserva = fields.Boolean(string="Reserva")
    
    