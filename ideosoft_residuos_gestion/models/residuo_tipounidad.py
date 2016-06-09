# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

    
    
class Tipo_Unidad(models.Model):
    
    _name = 'residuo.tipounidad'
    _description = 'Tipo de unidad'
    
    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s (%s)" % (record.descripcion, record.simbolo)))
        return result
    
    descripcion = fields.Char(string="Descripcion")
    simbolo = fields.Char(string="Simbolo")