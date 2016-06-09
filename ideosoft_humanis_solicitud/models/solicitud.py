# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

class Solicitud(models.Model):

    _name = 'hr.employee.solicitud'
    _description = "Solicitud"
    
    
    @api.multi
    def solicitud_print(self):
        return self.env['report'].get_action(self, 'ideosoft_humanis_solicitud.report_solicitud')
   

    employee_id = fields.Many2one('hr.employee', string="Empleado", ondelete='cascade', required=True)
    codigo = fields.Char(string="Código")
    tipo_solicitud_id = fields.Many2one('hr.employee.tiposolicitud', string="Tipo")
    descripcion = fields.Char(string="Descripción")
    fecha = fields.Date(string="Fecha")
    estado = fields.Selection([('al','ALTA'),('as','ASIGNADA'),('de','DESESTIMADA'),('fi','FINALIZADA'),('pe','PENDIENTE')], string='Estado', select=True, index=True, copy=False)
    

class TipoSolicitud(models.Model):

    _name = 'hr.employee.tiposolicitud'
    _description = 'Tipo de solicitud'

    code = fields.Char(string="Código")
    name = fields.Char(string="Descripción")