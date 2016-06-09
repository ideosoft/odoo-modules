# -*- coding: utf-8 -*-

from openerp import models, fields, api


class hr_contract_type(models.Model):
    _inherit = 'hr.contract.type'

    type_es_id = fields.Many2one(comodel_name='hr.contract.type.es', string='Tipo S. S.')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
