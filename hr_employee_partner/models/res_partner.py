# -*- coding: utf-8 -*-

from openerp import models, fields, api

class res_partner(models.Model):
    _inherit = 'res.partner'

    is_employee = fields.Boolean(string="Is a Employee")
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')

