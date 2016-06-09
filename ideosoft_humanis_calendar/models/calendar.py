# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime, timedelta
from openerp.exceptions import except_orm, Warning, RedirectWarning

import logging
_logger = logging.getLogger(__name__)

class IdeoCalendar(models.Model):

    _name = "hr.employee.ideocalendar"
    
    
    @api.model
    def getVacations(self, employee_id):
    
        result = []
        contract_id = []
        festivosc = []
        generales = []
        
        year = datetime.now().year
        
        if employee_id:
        
            # obtengo los días festivos (asociados al convenio)
            employee = self.env['hr.employee'].browse(int(employee_id))
            convenio = self.env['hr.employee.convenio'].search([('id','=',employee.convenio_id.id)])
            festconv = self.env['hr.employee.festivoconvenio'].search([('convenio_id','=',convenio.id)])
            
            # obtengo los festivos generales para esta año
            festgen = self.env['res.public_holiday'].search([('year','=',year)])
            for f in festgen:
                generales.append({
                    'date': datetime.strptime(f.date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'desc': f.name
                })
            
            for fest in festconv:
                festivosc.append(datetime.strptime(fest.date, '%Y-%m-%d').strftime('%d/%m/%Y'))

            # compruebo el contrato en vigor
            contracts = self.env['hr.contract'].search([('employee_id','=',int(employee_id))])
            
            if not contracts: 
                raise Warning('No existe un contracto activo sobre el que guardar las vacaciones')

            for contract in contracts:
            
                # no computo las prorrogas como contratos normales
                if not contract.es_prorroga:

                    # si no tiene fecha fin de contrato o si es mayor que hoy es el contrato en vigor
                    if not contract.date_end or (contract.date_end and datetime.strptime(contract.date_end,"%Y-%m-%d") > datetime.now()) or (contract.date_end_prorroga and datetime.strptime(contract.date_end_prorroga,"%Y-%m-%d") > datetime.now()):
                        
                        contract_id = contract.id
                        vacations = self.env['hr.employee.vacations'].search([('contract_id','=',contract_id)])
                        for day in vacations:
    
                            if day.type == '1':
                                type = 'c'
                            if day.type == '0.666666666':
                                type = 'm'
                            if day.type == '0.333333333':
                                type = 't'

                            result.append({
                                'date': datetime.strptime(day.date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                                'type': type
                            })
                            
                    else:
                        raise Warning('No existe un contracto activo sobre el que guardar las vacaciones')
                
        return {'vacations': result, 'contract_id': contract_id, 'generales': generales, 'festivosc': festivosc}
        
        
        
        
    @api.model
    def getFestivosconvenio(self, convenio_id):
    
        generales = []
        festivosc = []
        
        year = datetime.now().year
        
        if convenio_id:
        
            festconv = self.env['hr.employee.festivoconvenio'].search([('convenio_id','=',int(convenio_id))])
            for fest in festconv:
                print fest.date
                festivosc.append(datetime.strptime(fest.date, '%Y-%m-%d').strftime('%d/%m/%Y'))
                
            fests = self.env['res.public_holiday'].search([('year','=',year)])
            for f in fests:
                generales.append({
                    'date': datetime.strptime(f.date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    'desc': f.name
                })
            
        return {'generales': generales, 'festivosc': festivosc, 'year': year }
        
     
    def _compute_convenio_days(self, employee_id):
    
        employee = self.env['hr.employee'].browse(employee_id)
      
        if employee.convenio_id:
            convenio = self.env['hr.employee.convenio'].browse(employee.convenio_id.id)
            return convenio.vacation_days
        else:
            return 0
            
    
    def _compute_personal_days(self, employee_id):
    
        employee = self.env['hr.employee'].browse(employee_id)
      
        if employee.convenio_id:
            convenio = self.env['hr.employee.convenio'].browse(employee.convenio_id.id)
            return convenio.personal_days
        else:
            return 0
     
        
    def get_requested_days(self, contract_id):
        count = 0
        days = self.env['hr.employee.vacations'].search([('contract_id','=',contract_id)])
        if days:
            for d in days:
                count = count + float(d.type)
               
        return count
        
    
    def _compute_requested_days(self, employee_id):
    
        req_days = 0
        employee = self.env['hr.employee'].browse(int(employee_id))
    
        contracts = self.env['hr.contract'].search([('employee_id','=',employee.id)])
        for contract in contracts:  
            # no computo las prorrogas como contratos normales
            if not contract.es_prorroga:
                # si no tiene fecha fin de contrato o si es mayor que hoy es el contrato en vigor
                if not contract.date_end or (contract.date_end and datetime.strptime(contract.date_end,"%Y-%m-%d") > datetime.now()) or (contract.date_end_prorroga and datetime.strptime(contract.date_end_prorroga,"%Y-%m-%d") > datetime.now()):
                    req_days = self.get_requested_days(contract.id)
                    
        return req_days
                    
                    
    def _compute_previous_year_days(self, employee_id):
    
        employee = self.env['hr.employee'].browse(int(employee_id))
        
        if employee.previous_year_days:
            return employee.previous_year_days
        else:  
            return 0
                    
                    
    def _compute_annual_days(self, employee_id):
    
        employee = self.env['hr.employee'].browse(int(employee_id))
    
        contracts = self.env['hr.contract'].search([('employee_id','=',employee.id)])
        convenio = self.env['hr.employee.convenio'].browse(employee.convenio_id.id)
        
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
                        return delta.days * convenio.vacation_days / 365
                        
                    # la fecha de inicio NO pertenece al año actual                
                    else:
                        return convenio.vacation_days
                        
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
                            return delta.days * convenio.vacation_days / 365
                            
                        # la fecha de inicio NO pertenece al año actual                
                        else:
                            return convenio.vacation_days
                            
                    # si la fecha fin pertenece al año actual                
                    else:
                        # la fecha de inicio pertenece al año actual
                        if datetime.strptime(contract.date_start,"%Y-%m-%d").year == date.today().year:
                            delta = datetime.strptime(contract.date_end,"%Y-%m-%d") - datetime.strptime(contract.date_start,"%Y-%m-%d")
                            return delta.days * convenio.vacation_days / 365
                            
                        # la fecha de inicio NO pertenece al año actual
                        else:
                            delta = datetime.strptime(contract.date_end,"%Y-%m-%d") - datetime.strptime(str(date.today().year) + "-01-01","%Y-%m-%d")
                            return delta.days * convenio.vacation_days / 365
        
    
    def _compute_hanging_days(self, employee_id):
    
        hang_days = 0
    
        employee = self.env['hr.employee'].browse(int(employee_id))
    
        contracts = self.env['hr.contract'].search([('employee_id','=',employee.id)])
        convenio = self.env['hr.employee.convenio'].browse(employee.convenio_id.id)
        
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

                        hanging_days = float(delta.days * convenio.vacation_days / 365 - requested_days + self._compute_previous_year_days(employee.id))
                        
                        if hanging_days > 0:
                            hang_days = hanging_days 
                    
                    # si la fecha de inicio NO pertenece al año actual                
                    else:
                        hanging_days = convenio.vacation_days - requested_days + self._compute_previous_year_days(employee.id)
                        if hanging_days > 0:
                            hang_days = hanging_days
                        

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
                            
                            hanging_days = float(delta.days * convenio.vacation_days / 365 - requested_days + self._compute_previous_year_days(employee.id))
                            
                            if hanging_days > 0:
                                hang_days = hanging_days
                                
                        # la fecha de inicio NO pertenece al año actual             
                        else:
                            hanging_days = convenio.vacation_days - requested_days + self._compute_previous_year_days(employee.id)
                            if hanging_days > 0:
                                hang_days = hanging_days
                                
                    # si la fecha fin pertenece al año actual                
                    else:
                    
                        # la fecha de inicio pertenece al año actual
                        if datetime.strptime(contract.date_start,"%Y-%m-%d").year == date.today().year:

                            delta = datetime.strptime(contract.date_end,"%Y-%m-%d") - datetime.strptime(contract.date_start,"%Y-%m-%d")
           
                            hanging_days = float(delta.days * convenio.vacation_days / 365 - requested_days + self._compute_previous_year_days(employee.id))
                            
                            if hanging_days < 0:
                                hang_days = hanging_days
           
                        # la fecha de inicio NO pertenece al año actual
                        else:
                        
                            delta = datetime.strptime(contract.date_end,"%Y-%m-%d") - datetime.strptime(str(date.today().year) + "-01-01","%Y-%m-%d")

                            hanging_days = float(delta.days * convenio.vacation_days / 365 - requested_days + self._compute_previous_year_days(employee.id))
                            if hanging_days > 0:
                                hang_days = hanging_days
                                
        return hang_days
    
    
    @api.model
    def getDataDays(self, employee_id, aux=None):

        if employee_id:
        
            employee_id = int(employee_id)
            
            convenio_days = 0
            personal_days = 0
            annual_days = 0
            requested_days = 0
            hanging_days = 0
            previous_year_days = 0
                   
            convenio_days = self._compute_convenio_days(employee_id)
            personal_days = self._compute_personal_days(employee_id)
            annual_days = self._compute_annual_days(employee_id)
            
            if aux == None:
                previous_year_days = self._compute_previous_year_days(employee_id)
                requested_days = self._compute_requested_days(employee_id)
                hanging_days = self._compute_hanging_days(employee_id)
                
            else:               
                requested_days = self._compute_requested_days(employee_id) + aux
                if requested_days < 0:
                    requested_days = 0
                    
                previous_year_days = self._compute_previous_year_days(employee_id) - aux
                if previous_year_days < 0:
                    previous_year_days = 0
                
                hanging_days = annual_days - requested_days + self._compute_previous_year_days(employee_id)
                if hanging_days < 0:
                    hanging_days = 0
                    
            return {'convenio_days': convenio_days, 'personal_days': personal_days, 'requested_days': requested_days, 'annual_days': annual_days, 'previous_year_days': previous_year_days, 'hanging_days': hanging_days}
