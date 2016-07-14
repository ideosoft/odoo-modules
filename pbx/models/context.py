# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Context(models.Model):
    '''Context'''
    
    _name = "pbx.context"
    _description = "Context"
    
    name = fields.Char(string="Name")