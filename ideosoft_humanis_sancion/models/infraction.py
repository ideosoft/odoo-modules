# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

INFRACTION_STATES = [
    ('draft', 'Borrador'),
    ('confirm', 'Confirmado'),
    ('action', 'Sancionado'),
    ('noaction', 'No Sancionado'),
]

class InfractionCategory(models.Model):

    _name = 'hr.infraction.category'
    _description = 'Infraction Type'

    code = fields.Char(string="Código")
    name = fields.Char(string='Name', required=True)
   
class Infraction(models.Model):

    _name = 'hr.infraction'
    _description = "Sanción"

    name = fields.Char(string="Descripción")
    date = fields.Date(string="Fecha")
    category_id = fields.Many2one('hr.infraction.category', string='Categoria', required=False)
    employee_id = fields.Many2one('hr.employee', string="Empleado", ondelete='cascade')
    state = fields.Selection(selection=INFRACTION_STATES,string='Estado', default='draft')
    attached = fields.Binary(string="Adjunto")
    memo = fields.Text(string="Notas")