# -*- coding: utf-8 -*-

import pprint
from pprint import pprint

import openerp
from openerp.addons.web import http
from openerp.http import request

class ToolController(openerp.http.Controller):
    @http.route('/tools/update/<module>',
        auth='user')
    def handler(self, module):

        module_obj = request.registry['ir.module.module']
    
        ids = module_obj.search(request.cr, request.uid, [('name', 'ilike', module), ('state', '=', 'installed')], context=request.context)
        
        r = False
        
        try:
            r = module_obj.button_immediate_upgrade(request.cr, request.uid, ids, context=request.context)
        except Exception:
            pass
        
        return "Ok"