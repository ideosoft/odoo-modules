# -*- coding: utf-8 -*-
from openerp import models, fields, api
from pprint import pprint

class Company(models.Model):
    _inherit = 'res.company'

    parent_receivable_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Receivable Account',
        domain="[('type','=','view'),('company_id','=',active_id)]",
        help='If set, a receivable account will be created for all partners with the "Customer" flag set.')
        
    parent_payable_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Payable Account',
        domain="[('type','=','view'),('company_id','=',active_id)]",
        help='If set, a payable account will be created for all partners with the "Supplier" flag set.')
        
    account_digits = fields.Integer(
        string='Number of digits',
        help='Indicates the number of digits to be used for automatically created receivable and payable partner accounts.')