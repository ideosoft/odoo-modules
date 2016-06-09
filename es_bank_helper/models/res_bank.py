# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions

class ResBank(models.Model):
    _inherit = 'res.bank'

    code = fields.Char('Code', size=64)
    lname = fields.Char('Long name', size=128)
    vat = fields.Char('VAT code', size=32, help='Value Added Tax number')
    website = fields.Char('Website', size=64)