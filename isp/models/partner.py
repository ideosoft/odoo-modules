# -*- encoding: utf-8 -*-

from openerp import api, fields, models

class Partner(models.Model):
    
    _inherit = 'res.partner'
    
        
    def _count_services(self):
        self.count_services = 717
        
        
    count_services = fields.Integer(compute='_count_services')
    
    service_ids = fields.One2many(comodel_name='contract.service', inverse_name='partner_id', string='Contracts')
    
    main_contract_id = fields.Many2one(comodel_name='account.analytic.account')
    main_contract_state = fields.Selection(related='main_contract_id.state')
    main_contract_date_start = fields.Date(related='main_contract_id.date_start')
    
    