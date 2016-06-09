# -*- coding: utf-8 -*-

from openerp import models, fields, api
        
class MikrotikImport(models.TransientModel):

    _name = "radius.mikrotik.import"
    _description = "Mikrotik Import"
    
    @api.multi
    def action_import(self):
        self.status = "OK!"
        
    
    @api.onchange('password')
    def action_import(self):
        if(self.host and self.username and self.password):
            apiros = ApiRos(s);
            apiros.login(self.username, self.password);
            apiros.writeSentence(['/ppp/secret/getall'])
            pprint(apiros.readSentence())

    host = fields.Char(string='Host', default='217.197.22.1')
    port = fields.Char(string='Port', default='8728')
    username = fields.Char(string='Username', default='admin')
    password = fields.Char(string='Password')
    status = fields.Char(string='Status')
   
       
