# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Manufacturer(models.Model):
    """pbx provision"""
    
    _name = 'pbx.provision.device'
    _description = "Provision Device"

    name = fields.Char(string='MAC', size=64, required=True)
    model_id = fields.Many2one(comodel_name='pbx.provision.device.model', string='Model')
    line = fields.Integer(string="Line")
    sipaccount_id = fields.Many2one(comodel_name='pbx.sipaccount', string='Sip')