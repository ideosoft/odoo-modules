# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

class Observacion(models.Model):

	_name = 'hr.employee.observacion'
	_description = "Observación"

	employee_id = fields.Many2one('hr.employee', string="Empleado", ondelete='cascade')
	codigo = fields.Char(string="Código")
	fecha = fields.Date(string="Fecha")
	hora = fields.Char(string="Hora")
	descripcion = fields.Text(string="Descripción")