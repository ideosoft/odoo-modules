# -*- coding: utf-8 -*-

from openerp import models, fields, api

class res_employee(models.Model):
    _inherit = 'hr.employee'

    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner')
    bank_ids = fields.One2many(comodel_name='res.partner.bank', inverse_name='employee_id', string='Banks')
    
    @api.model
    def create(self, vals):
        if not vals.get('name', False) or vals.get('partner_id', False):
            return super(res_employee, self).create(vals)
            
        obj_partner = self.env['res.partner']
        partner_id = obj_partner.create({'name': vals['name'], 'is_employee':True})
        
        vals.update({'partner_id': partner_id.id})
        employee_id = super(res_employee, self).create(vals)
        
        obj_partner.write({'employee_id': employee_id.id})
        return employee_id
        
        
    
    @api.multi
    def write(self, vals):
        # if vals.get('name', False):
            # print "*" * 80
            # print self.env['res.partner'].browse([self.id])
            # self.env['res.partner'].browse([self.id]).write({'name': vals['name']})
            # print "*" * 80
        
        return super(res_employee, self).write(vals)