# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

class Sueldo(models.Model):

	_name = 'hr.employee.sueldo'
	_description = "Sueldo"

	employee_id = fields.Many2one('hr.employee', string="Empleado", ondelete='cascade')
	fecha = fields.Date(string="Fecha")
	ajustado = fields.Char(string="Sueldo ajustado")
	num_pagas = fields.Integer(string="Número de pagas")
	sba = fields.Integer(string="Sueldo bruto anual (SBA) Euros")