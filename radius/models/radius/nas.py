# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Nas(models.Model):
    _name = "radius.nas"
    _description = "Nas"

    nasname = fields.Char(string='IP/Host', size=128)
    shortname = fields.Char(string='Shortname', size=32)
    type =  fields.Selection([('cisco','cisco'),('portslave','portslave'),('other','other')], string='Type', size=32, default='other')
    ports = fields.Integer(string='Ports')
    secret = fields.Char(string='Secret', size=64)
    community = fields.Char(string='Community', size=64)
    description = fields.Text(string='Description')