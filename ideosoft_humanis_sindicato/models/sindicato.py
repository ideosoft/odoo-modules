# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

class Sindicato(models.Model):

	_name="hr.employee.sindicato"
	_description="Sindicato"

	name = fields.Char(string="Nombre", required=True)
	employee_id = fields.Many2one('hr.employee', string='Empleado', ondelete='set null')