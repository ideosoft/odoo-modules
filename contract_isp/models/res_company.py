# -*- coding: utf-8 -*-

from openerp import models, fields, api

class res_company(models.Model):
    _inherit = 'res.company'

    def _cutoff_days(self):
        return [(str(x), str(x)) for x in range(1, 31)]

    cutoff_day = fields.Selection(selection='_cutoff_days', string='Cutoff day')
    parent_account_id = fields.Many2one(comodel_name='account.analytic.account', string='Parent Analytic Account')
    default_journal_id = fields.Many2one(comodel_name='account.analytic.journal', string='Default Journal')