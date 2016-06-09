# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

class experience(models.Model):

	_name = "hr.employee.experience"
	_description = "Experiencia laboral"

	employee_id = fields.Many2one('hr.employee', string="Empleado", ondelete='cascade')
	fecha_inicio = fields.Date(string="Fecha inicio")
	fecha_fin = fields.Date(string="Fecha fin")
	puesto = fields.Char(string="Puesto")
	empresa = fields.Char(string="Empresa")