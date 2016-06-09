# -*- coding: utf-8 -*-

import openerp

from openerp.osv import osv, fields
from openerp.tools.translate import _

class contract_service(osv.Model):
    _name = 'contract.service'

    _columns = {
        'activation_date': fields.datetime('Activation date'),
        'duration': fields.integer('Duration'),
        'product_id': fields.many2one('product.product',
                                      'Product',
                                      required=True),
        'qty': fields.float(
            'Qty'),
        'category_id': fields.many2one('product.category', 'Product Category'),
        'name': fields.char('Description', size=64),
        'analytic_line_type': fields.selection((('r', 'Recurrent'),
                                                ('x', 'Exception'),
                                                ('o', 'One time')),
                                               'Type'),
        'require_activation': fields.boolean('Require activation'),
        'account_id': fields.many2one('account.analytic.account', 'Contract'),
        'unit_price': fields.float(
            string='Unit Price'),
        'price': fields.float(
            string='Price'),
        'activation_line_generated': fields.boolean(
            'Activation Line Generated?'),
        'state': fields.selection((('draft', 'Waiting for activating'),
                                   ('active', 'Active'),
                                   ('inactive', 'Inactive')),
                                  'State')
    }
    
    _defaults = {
    }

class account_analytic_account(osv.Model):
    _name = "account.analytic.account"
    _inherit = "account.analytic.account"

    _columns = {
        'contract_service_ids': fields.one2many('contract.service',
                                                'account_id',
                                                'Services'),
        'use_contract_services': fields.boolean('Contract services'),
        'state': fields.selection([('template', 'Template'),
                                   ('draft', 'New'),
                                   ('open', 'In Progress'),
                                   ('pending', 'Suspended'),
                                   ('close', 'Closed'),
                                   ('cancelled', 'Cancelled')],
                                  'Status', required=True,
                                  track_visibility='onchange'),
    }

    _defaults = {
        'use_contract_services': False
    }