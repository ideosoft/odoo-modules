# -*- coding: utf-8 -*-

from openerp import models, fields, api

class res_partner_bank(models.Model):
    _inherit = 'res.partner.bank'

    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', ondelete='cascade', help="Only if this bank account belong to employee")
    
    
    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if self.employee_id:
            if self.employee_id.partner_id:
                self.partner_id = self.employee_id.partner_id
                
        

    # @api.model
    # def create(self, vals):
        # return super(res_partner_bank, self).create(vals)