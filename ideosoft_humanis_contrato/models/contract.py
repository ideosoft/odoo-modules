# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime, timedelta
from openerp.exceptions import except_orm, Warning, RedirectWarning

import logging
_logger = logging.getLogger(__name__)

class Contract(models.Model):

    _name = 'hr.contract'
    _inherit = 'hr.contract'
    
    
    def _calculate_name(self):
        employee = self.env['hr.employee'].browse(self.env.context['default_employee_id'])
        contracts = self.env['hr.contract'].search([('employee_id','=',employee.id)])
        return 'CON/' + str(employee.id).zfill(5) + "-" + str(len(contracts)+1)
        
    @api.one
    @api.onchange('type_id')
    def onchange_type(self):
        if self.type_id:
            type = self.env['hr.contract.type'].browse(self.type_id.id)
            if type.code == 'F': # INDEFINIDO
                self.date_end = ''
                

    @api.model
    def update_contract_state(self):
    
        print '********** EJECUTANDO ACTUALIZACION DE CONTRATOS ***********'
        
        active_contracts = self.env['hr.contract'].search([('is_active','=',True)])
        for contract in active_contracts:
            if((not contract.date_end_prorroga and contract.date_end and datetime.strptime(contract.date_end,"%Y-%m-%d") < datetime.now()) or (contract.date_end_prorroga and datetime.strptime(contract.date_end_prorroga,"%Y-%m-%d") < datetime.now())):
            
                print 'Id: %d - Codigo: %s --> Desactivado' % (contract.id, contract.name)
                contract.is_active = False
                
                
    @api.multi
    def write(self, vals):
        
        if 'extendable' in vals and vals['extendable'] == False:
            vals['date_end_prorroga'] = None
           
        contract = super(Contract, self).write(vals)

        if self.es_prorroga:
            eventual = self.env['hr.contract'].browse(self.eventual_id.id)
            eventual.date_end_prorroga = self.date_end

        return contract
    
    
    
    name = fields.Char(default=_calculate_name)
    
    date_baja = fields.Date(string="Fecha Baja")
    motivo_baja = fields.Char(string="Motivo Baja")
    inem = fields.Boolean(string="Registrado INEM")
    entregado = fields.Boolean(string="Entregado")
    workweek = fields.Char(string="Jornada Semanal")
    notes = fields.Text("Notas")
    # empresa_id = fields.Many2one(comodel_name="res.company", string="Empresa")
    centrotrabajo_id = fields.Many2one(comodel_name="res.company.area.servicio.centrotrabajo", string="Centro trabajo", required=True)
    
    es_prorroga = fields.Boolean("Es prórroga")
    date_end_prorroga = fields.Date(string="Fecha fin prórroga")
    eventual_id = fields.Many2one(comodel_name="hr.contract", string="Eventual (contrato padre)")
    
    hanging_days_paid = fields.Boolean(string="Días restantes pagados", default=False)
    is_active = fields.Boolean(string="Activo", default=True)
    
    extendable = fields.Boolean(related='type_id.extendable')
    
    
    _sql_constraints = [
        ('name', 'unique(name)', 'Esa referencia de contrato ya existe. Avisar al administrador.')
    ]
    

    
class ContractType(models.Model):

    _name = 'hr.contract.type'
    _inherit = 'hr.contract.type'
    
    code = fields.Char(string="Código")
    extendable = fields.Boolean("Prorrogable")
    
    
class ContractWizard(models.TransientModel):

    _name = 'hr.wizardcontract'
    _description = 'Wizard'

    def _calculate_startdate(self):
        contract = self.env['hr.contract'].browse(self.env.context['active_id'])
        if contract.date_end_prorroga:
            date = datetime.strptime(contract.date_end_prorroga,"%Y-%m-%d") + timedelta(days=1)
        else:
            date = datetime.strptime(contract.date_end,"%Y-%m-%d") + timedelta(days=1)
        return date
        
    
    start_date = fields.Date(string="Fecha inicio", default=_calculate_startdate)
    finish_date = fields.Date(string="Fecha fin")
    
    @api.one
    def setProrroga(self):
        contract = self.env['hr.contract'].browse(self.env.context['active_id'])
        contracts = self.env['hr.contract'].search([('employee_id','=',contract.employee_id.id)])
        next = self.env['ir.sequence'].next_by_code('hr.contract.seq')
        type = self.env['hr.contract.type'].search([('code','=','PRR')])
        
        if self.start_date and self.finish_date and (self.finish_date >= self.start_date):

            new = self.env['hr.contract'].create({
                'name': next + str(contract.employee_id.id).zfill(3) + "-" + str(len(contracts)+1),
                'date_start': self.start_date,
                'date_end': self.finish_date,
                'centrotrabajo_id': contract.centrotrabajo_id.id,
                #'empresa_id': contract.empresa_id.id,
                'employee_id': contract.employee_id.id,
                'type_id': type.id,
                'wage': contract.wage,
                'eventual_id': contract.id,
                'es_prorroga': True
            })
            
            if not contract.date_end_prorroga or contract.date_end_prorroga < new.date_end:
                
                contract.write({
                    'date_end_prorroga': new.date_end
                })
        
        else:
            raise Warning("La fecha FIN debe ser mayor que la fecha INICIO")
         