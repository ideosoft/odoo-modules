# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

class Recurso(models.Model):

    _name = 'hr.employee.recurso'
    _description = "Recurso"

    employee_id = fields.Many2one('hr.employee', string="Empleado", ondelete='cascade')
    fecha_entrega = fields.Date(string="Fecha entrega")
    tipo_recurso_id = fields.Many2one('hr.employee.tiporecurso', string="Tipo")
    descripcion = fields.Char(string="Descripción")
    fecha_devol = fields.Date(string="Fecha devolución")
    
    
class TipoRecurso(models.Model):

    _name = 'hr.employee.tiporecurso'
    _description = 'Tipo de recurso'

    code = fields.Char(string="Código")
    name = fields.Char(string="Descripción")