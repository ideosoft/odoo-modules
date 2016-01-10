# -*- encoding: utf-8 -*-

from openerp import api, fields, models
   
class ContractService(models.Model):

    _inherit = 'contract.service'
    
    value = fields.Char(string='Associacion')
    
    partner_id = fields.Many2one(comodel_name='res.partner',string='Customer', related='account_id.partner_id', store=True)
