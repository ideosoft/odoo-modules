# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

class Puesto(models.Model):

    _name = 'hr.employee.puesto'
    _description = "Puesto"

    employee_id = fields.Many2one('hr.employee', string="Empleado", ondelete='cascade')
    puesto = fields.Char(string="Puesto")
    categoria_puesto_id = fields.Many2one('hr.employee.categoriapuesto', string="Categoría")
    fecha_alta = fields.Date(string="Fecha alta")
    fecha_baja = fields.Date(string="Fecha baja")
    
    
class CategoriaPuesto(models.Model):

    _name = 'hr.employee.categoriapuesto'
    _description = 'Categoria puesto'

    code = fields.Char(string="Código")
    name = fields.Char(string="Descripcion")
