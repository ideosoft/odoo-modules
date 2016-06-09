# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

class Cita(models.Model):

	_name="hr.employee.cita"
	_description="Citas"

	employee_id = fields.Many2one('hr.employee', string='Empleado', ondelete='cascade')
	fecha = fields.Date(string="Fecha")
	hora = fields.Char(string="Hora")
	lugar = fields.Char(string="Lugar")
	cc = fields.Boolean(string="Cancelada")
	pst = fields.Boolean(string="Presentado")
	descripcion = fields.Text(string="Descripción")
	estado = fields.Boolean(string="Reserva")