# -*- coding: utf-8 -*-

import string
import random

from openerp import models, fields, api, _
from Asterisk import Manager

PASS_GENERATOR = string.ascii_uppercase + string.ascii_lowercase + string.digits


    

    
class Dialplan(models.Model):
    
    _name = "pbx.dialplan"
    _description = "pbx Dialplan"

    name = fields.Char(string='Dialplan', size=50, required=True)


class Sipaccount(models.Model):
    
    _name = "pbx.sipaccount"
    _description = "pbx Sip Account"
    
    @api.multi
    def _compute_tech(self):
        for record in self:
            record.tech = "SIP/%s" % record.name
    
    def _generate_pass(self):
        return ''.join(random.choice(PASS_GENERATOR) for i in range(16))

    name = fields.Char(string='Username', size=50, required=True)
    password = fields.Char(string='Password', size=50, default=_generate_pass)
    callerid = fields.Char(string='Callerid', size=50)
    
    tech = fields.Char(string="Tech", compute='_compute_tech')
    
    dialplan = fields.Many2one('pbx.dialplan', string="Dialplan")

