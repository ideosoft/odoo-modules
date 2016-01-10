# -*- coding: utf-8 -*-

from openerp import models, fields

class account_analytic_line(models.Model):
    _inherit = 'account.analytic.line'

    contract_service_id = fields.Many2one(comodel_name='contract.service', string='Service')
    is_prorata = fields.Boolean(string='Prorata', default=False)

