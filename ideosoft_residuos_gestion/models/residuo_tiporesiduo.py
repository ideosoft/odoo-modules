# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

class Tipo_Residuo(models.Model):

    _name = 'residuo.tiporesiduo'
    _description = 'Tipo de residuo'

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s" % (record.descripcion)))
        return result

    descripcion = fields.Char(string="Descripcion")
    unidad = fields.Many2one('residuo.tipounidad', string='Unidad', ondelete='set null', select=True)
    codler = fields.Many2one('residuo.codigoler', string='Codigo LER', ondelete='set null', select=True)
    peso = fields.Float(string="Peso Estimado (Kg)", default=0, store=True)
    