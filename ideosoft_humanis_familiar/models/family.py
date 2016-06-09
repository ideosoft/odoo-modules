# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

MINUSVALIA_VALORES = [
    ('0','-'),
    ('1','33-65'),
    ('2','65-100'),
]

class Family(models.Model):

    _name = 'hr.employee.family'
    _description = "Familiar"
    
    @api.one
    @api.depends('birthday')
    def _compute_age(self):
        if self.birthday:
            age = int((datetime.now()-datetime.strptime(self.birthday,"%Y-%m-%d")).days/365.25)
            if age < 0:
                age = 0
            self.age = age
        else:
            self.age = 0
            
            
            
        
    employee_id = fields.Many2one(comodel_name='hr.employee', string="Empleado", ondelete='cascade')
    name = fields.Char(string="Descripción")
    relationship = fields.Selection(string="Parentesco", selection=[
        ('father', 'Padre'),
        ('mother', 'Madre'),
        ('child', 'Hij@'),
        ('spouse', 'Conyuge'),
        ('partner', 'Pareja')
    ])
    birthday = fields.Date(string="Nacimiento")
    age = fields.Integer(string="Edad", compute=_compute_age, default=0)
    phone = fields.Char(string="Telefono")
    minusvalia = fields.Selection(MINUSVALIA_VALORES, string="Minusvalía", default='0')