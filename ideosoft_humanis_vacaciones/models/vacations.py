# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime, timedelta as td
from openerp.exceptions import except_orm, Warning, RedirectWarning

import re

import logging
_logger = logging.getLogger(__name__)

TYPE = [('1', 'Completo'), ('0.666666666', 'Mañana'), ('0.333333333', 'Tarde')]


class Vacations(models.Model):

    _name="hr.employee.vacations"
    _description="Vacaciones"
    
    date = fields.Date(string="Día de vacaciones", required=True)
    type = fields.Selection(TYPE, string="Tipo", default="1")
    contract_id = fields.Many2one(comodel_name="hr.contract", string="Contrato", required=True, ondelete="cascade")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Empleado", ondelete="cascade", required=True)

    
    @api.model
    def create(self, values):
    
        # Compruebo que no exista ese dia para el mismo contrato
        if self.env['hr.employee.vacations'].search([('contract_id','=',values['contract_id']),('date','=',values['date'])]):
            raise Warning("Ya existe el día " + values['date'].strftime('%d/%m/%Y') + " para este contrato")
        else:
            id = super(Vacations, self).create(values)
            return id
            
            
        
class VacationsWizard(models.TransientModel):

    _name = 'hr.employee.vacationswizard'
    _description = 'Wizard'
    

    vacation_id = fields.Many2one('hr.employee.vacations', string='Día de vacaciones')
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Empleado")
    contract_id = fields.Integer(string="Contrato id")
    allow_saturdays = fields.Boolean(string="Habilitar sábados")
    allow_sundays = fields.Boolean(string="Habilitar domingos")
    allow_holidays = fields.Boolean(string="Habilitar festivos")
    aux_dates = fields.Char(string="string_fechas")
    previous_days = fields.Char(string="campo auxiliar dias años anteriores")
    
    
    
    def _totype(self, type):
        if type == 'c':
            return '1'
        elif type == 'm':
            return '0.666666666'
        elif type == 't':
            return '0.333333333'
    

    @api.one
    @api.depends('vacation_id','aux_dates','previous_days')
    def setVacations(self):
        
        # compruebo que se encuentra seleccionado un empleado
        self.employee_id = self.env.context['active_id']
        employee = self.env['hr.employee'].browse(self.employee_id.id)
        
        if self.previous_days: 
            employee.previous_year_days = self.previous_days
        
        if not self.employee_id:
            raise Warning("No hay ningún empleado seleccionado")
        
        # sustituyo los dias viejos por los nuevos
        if self.contract_id:

            actual_vacations = self.env['hr.employee.vacations'].search([('contract_id','=',self.contract_id)])
            
            for vaca in actual_vacations:
                vaca.unlink()

            if self.aux_dates:
                for vacation in self.aux_dates.split(','):
                    
                    day =  vacation[:10]
                    type = vacation[10:]
                    
                    date = datetime.strptime(day,"%d/%m/%Y")
                    
                    vacation_day = self.env['hr.employee.vacations'].create({
                        'date': date,
                        'type': self._totype(type),
                        'contract_id': self.contract_id,
                        'employee_id': self.employee_id.id
                    })
                    
                    
                # refresh parent view
                return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }    

        else:
            raise Warning("No se ha podido guardar las vacaciones del empleado. No tiene ningún contrato válido.")
            
    

    @api.multi
    def printVacations(self):
        
        if not self.aux_dates: 
            raise Warning('No se han solicitado ningunas vacaciones.')
    
        return self.env['report'].get_action(self, 'ideosoft_humanis_vacaciones.report_vacaciones')
    

class AdjustVacationsWizard(models.TransientModel):

    _name = 'hr.employee.adjustvacationswizard'
    _description = 'Wizard'
    
    num_days = fields.Float(string="Número de días", digits=(10, 2))
    to_pay = fields.Boolean(string="Marcar como pagados", default=False)
    
    
    def adjustDecimals(self, val):
        
        dec = str(val)[-2:]
        
        if(dec == '32' or dec == '65' or dec == '99'):
            if val > 0:
                val = val + 0.01
            else:
                val = val - 0.01

        if(dec == '34' or dec == '67' or dec == '01'):
            if val > 0:
                val = val - 0.01
            else:
                val = val + 0.01

        return val

  

    @api.one
    def setAdjustDays(self):
    
        employee_id = self.env.context['active_id']
                
        if employee_id:
            employee = self.env['hr.employee'].browse(employee_id)
            
            if self.num_days != 0:
                      
                numDays = self.num_days/100
                                
                employee.previous_year_days = employee.previous_year_days + numDays
                employee.previous_year_days = self.adjustDecimals(employee.previous_year_days)
                                
                # annotation in vacation_notes
                now = datetime.strftime(date.today(), '%d/%m/%Y')
                
                if employee.vacation_notes:
                    actual_notes = employee.vacation_notes + '\n'
                else:
                    actual_notes = ''
                    
                if numDays > 0:
                    new_notes = '%s [%s]: Registro de ajuste de dias: se suman %s dias' % (actual_notes,str(now),str(numDays))
                else:
                    if self.to_pay:
                        new_notes = '%s [%s]: Registro de ajuste de dias: se restan %s dias y se marcan como PAGADOS' % (actual_notes,str(now),str(numDays)[1:])
                    else:
                        new_notes = '%s [%s]: Registro de ajuste de dias: se restan %s dias' % (actual_notes,str(now),str(numDays)[1:])
               
                employee.vacation_notes = new_notes
                
                # refresh parent view
                # return {
                    # 'type': 'ir.actions.client',
                    # 'tag': 'reload',
                # }

                return { 'type' :  'ir.actions.act_close_wizard_and_reload_view' }
    
        else:
            raise Warning("No hay ningún empleado seleccionado")
    
    
    
    
    
      
        # if self.num_days != 0:

            # employee_id = self.env.context['active_id']
            # employee = self.env['hr.employee'].browse(employee_id)
            
            # if employee.previous_year_days > 0:
                # if self.num_days > 0 and employee.previous_year_days > self.num_days:
                    # employee.previous_year_days = employee.previous_year_days - self.num_days
                
            # contract_name = []
            
            # if not employee:
                # raise Warning("No hay ningún empleado seleccionado")
                   
            # now = datetime.strftime(date.today(), '%d/%m/%Y')
            
            # contracts = self.env['hr.contract'].search([('employee_id','=',employee_id)])
            # for contract in contracts:
                # if contract.is_active and not contract.es_prorroga:
                    # contract_name = contract.name

            # if employee.vacation_notes:
                # actual_notes = employee.vacation_notes + '\n'
            # else:
                # actual_notes = ''
                
            # if self.num_days == 1:
                # new_notes = actual_notes + '[' + str(now) + '] - Registro de adjuste de ' + str(self.num_days) + ' dia pagado. ID contrato: ' + contract_name
            # else:
                # new_notes = actual_notes + '[' + str(now) + '] - Registro de ' + str(self.num_days) + ' dias pagados. ID contrato: ' + contract_name
           
            # employee.vacation_notes = new_notes
        
        # else:
            # raise Warning("El número de días debe ser distinto de 0.")