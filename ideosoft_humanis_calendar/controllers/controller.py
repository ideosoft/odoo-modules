#-*- coding:utf-8 -*-

from openerp import http
from openerp.http import request


class CalendarController(http.Controller):


    @http.route('/assign_vacations', type='http', auth='user')
    def set_vacations(self, employee_id, date):
    
        print '**************************************'
        print '**************************************'
        
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry

        # compruebo que se encuentra seleccionado un empleado
        if employee_id:
        
            employee = pool['hr.employee'].browse(cr, uid, int(employee_id), context=context)
        

        
        print '**************************************'
        print '**************************************'
        
    