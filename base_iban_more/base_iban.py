# -*- coding: utf-8 -*-

import string
from pprint import pprint

from openerp import api, fields, models

class PartnerBank(models.Model):
    
    _name = "res.partner.bank"
    _inherit = "res.partner.bank"
    
    @api.one
    @api.onchange('acc_number')
    def onchange_acc_number(self):
        print "DEBUG: res.partner.bank.onchange_acc_number)()"
        if self.state == 'bank':
            number = self.acc_number.replace(' ','')
            bank = number[0:4]
            office = number[4:8]
            dc = number[8:10]
            account = number[10:20]
            
            bank = self.env['res.bank'].search([['code', '=', bank]], limit=1)

            if bank:
                self.bank = bank

    @api.one
    @api.onchange('bank')
    def onchange_bank(self):
        if self.bank:
            self.bank_name = self.bank.name
            self.bank_bic = self.bank.bic
    
    @api.returns('res.country')
    def _get_default_country(self):
        return self.env.user.company_id.country_id
    
    bank_country_id = fields.Many2one(comodel_name='res.country',string="Country", default=_get_default_country)

class Bank(models.Model):
    
    _name = "res.bank"
    _inherit = "res.bank"
    
    code = fields.Char('Code', size=64)
    lname = fields.Char('Long name', size=128)
    vat = fields.Char('VAT code', size=32, help='Value Added Tax number')
    website = fields.Char('Website', size=64)
            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
