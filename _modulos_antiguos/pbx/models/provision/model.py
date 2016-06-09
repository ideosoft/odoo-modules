# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Model(models.Model):
    """pbx provision"""
    
    _name = 'pbx.provision.device.model'
    _description = "Device Model"

    name = fields.Char(string='Name', size=64, required=True)
    manufacturer_id = fields.Many2one(comodel_name='pbx.provision.device.manufacturer', string='Manufacturer')
    lines = fields.Integer(string='Lines')
    template = fields.Text(string='Template')
