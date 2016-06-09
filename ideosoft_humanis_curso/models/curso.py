# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import date, datetime

class Curso(models.Model):

    _name = 'hr.employee.curso'
    _description = "Curso"
    
    codigo = fields.Char(string="Código", required=True, index=True)
    descripcion = fields.Text(string="Curso")
    horas = fields.Float(string="Horas")
    
    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s - %s" % (record.codigo, record.descripcion)))
        return result

        
class CursoEmpleado(models.Model):

    _name = 'hr.employee.cursoempleado'
    _description = "Curso empleado"
    
    curso_id = fields.Many2one('hr.employee.curso', string="Curso", ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', string="Empleado", ondelete='cascade')
    fecha = fields.Date(string="Fecha de realización")
    horas = fields.Float(related="curso_id.horas", string="Horas")