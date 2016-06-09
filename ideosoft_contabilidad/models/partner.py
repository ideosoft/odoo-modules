# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import date, datetime
import odoo

from pprint import pprint
import logging

_logger = logging.getLogger(__name__)



class Partner(models.Model):
    _description = 'Partner'
    _name = "res.partner"
    _inherit = "res.partner"

    @api.model
    def create(self, vals):

        partner = super(Partner, self).create(vals)
        
        if partner.customer:
            # self.create_account(partner.ids[0], 'receivable')
            pass
        if partner.supplier:    
            # self.create_account(partner.ids[0], 'payable')
            pass
            
        return partner

        
    @api.multi
    def write(self, vals):
    
        partner = super(Partner, self).write(vals)
        
        if 'customer' in vals or 'name' in vals:
            if self.property_account_receivable.partner_id and self.id == self.property_account_receivable.partner_id.id:
                self.property_account_receivable.write({'name': vals['name']})
        if 'supplier' in vals or 'name' in vals:
            if self.property_account_payable.partner_id and self.id == self.property_account_payable.partner_id.id:
                self.property_account_payable.write({'name': vals['name']})
        
        return partner
        
        
    @api.model
    def create_account(self, partner_id, account_type):
    
        if account_type not in ('receivable', 'payable'):
            return
                      
        company = self.env.user.company_id
        partner = self.browse(partner_id)
        
        if not (partner.customer or partner.supplier):
            return
        
        
        digits = company.account_digits or 0
        parent_account = getattr(company, 'parent_%s_account_id' % account_type)
        
        if partner.customer: 
            next = self.env['ir.sequence'].next_by_code('account.partner.seq_customer')
        else:
            next = self.env['ir.sequence'].next_by_code('account.partner.seq_supplier')
        
        if next:
            number = next
        else:
            number = partner.ref or str(partner.id)
        
        code = parent_account.code + '0'*(digits - len(parent_account.code + number)) + number
        
        account_id = self.env['account.account'].create({
            'name': partner.name,
            'code': code,
            'parent_id': parent_account.id,
            'user_type': parent_account.user_type.id,
            'reconcile': True,
            'type': account_type,
            'partner_id': partner.id
        })

        partner.write({
            'property_account_%s' % account_type : account_id,
        })
        
        return account_id

