# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

class Embargo(models.Model):

	_name = 'hr.employee.embargo'
	_description = "Embargo"

	employee_id = fields.Many2one('hr.employee', string="Empleado", ondelete='cascade')
	codigo = fields.Char(string="Código")
	organizacion = fields.Char(string="Organización")
	fecha_notif = fields.Date(string="Fecha notificación")
	importe = fields.Float(string="Importe")
	fecha_lev = fields.Date(string="Fecha levantamiento")
	fecha_liq = fields.Date(string="Fecha liquidación")
	observaciones = fields.Text(string="Observaciones")