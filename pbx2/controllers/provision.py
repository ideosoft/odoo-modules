# -*- coding: utf-8 -*-
from openerp import http

class Provision(http.Controller):

     @http.route('/provision/<model("pbx.provision.device"):obj>/', auth='public')
     def object(self, obj, **kw):
        
        
         return "OK";
