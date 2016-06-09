# -*- coding: utf-8 -*-

from openerp import models, fields, api

RADIUS_ATTRIBUTE_CHECK =[
    ('Cleartext-Password', 'Cleartext-Password'),
    ('Auth-Type', 'Auth-Type')
]


class Check(models.Model):
    _name = "radius.check"
    _description = "check"    
    _inherit = "radius.attribute"

    def _compute_display_name(self):
        name = "%s" % (self.username)
        self.display_name = name
        
    username = fields.Char(string='Username', size=64, select=1)
    attribute = fields.Selection(RADIUS_ATTRIBUTE_CHECK, string='Attribute')       
