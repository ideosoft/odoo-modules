# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

class Phone(models.Model):

    _name="hr.employee.phone"
    _description="Teléfono"
    
    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s" % (record.number)))
        return result
        

    number = fields.Char(string="Número")
    activ_date = fields.Date(string="Fecha alta")
    leave_date = fields.Date(string="Fecha baja")
    pin = fields.Char(string="PIN")
    puk = fields.Char(string="PUK")