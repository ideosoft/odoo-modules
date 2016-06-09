# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Account(models.Model):
    _inherit = 'account.account'
    _name = 'account.account'
    
    partner_id = fields.Many2one(comodel_name='res.partner', string='Asociado')