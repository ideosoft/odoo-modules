# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Manufacturer(models.Model):
    """pbx provision"""
    
    _name = 'pbx.provision.device.manufacturer'
    _description = "Device Manufacturer"

    name = fields.Char(string='Name', size=64, required=True)
