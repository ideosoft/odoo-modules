# -*- coding: utf-8 -*-

from openerp import models, fields, api

class res_partner(models.Model):
    _inherit = 'res.partner'

    partner_analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Partner Analytic Account')
 

    @api.model
    def create(self, vals, context=None):
        account_analytic_account = self.env['account.analytic.account']
        
        res_company = self.env['res.company']

        partner = super(res_partner, self).create(vals)

        account = account_analytic_account.create({
            'name': vals['name'],
            'parent_id': self.env.user.company_id.parent_account_id.id,
            'type': 'view',
            'partner_id': partner.id,
            'user_id': self.env.user.id
        })

        partner.write({'partner_analytic_account_id': account.id})

        return partner
