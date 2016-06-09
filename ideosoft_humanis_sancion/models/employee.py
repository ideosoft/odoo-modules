# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

class Employee(models.Model):

    _name = 'hr.employee'
    _inherit = 'hr.employee'

    infraction_ids = fields.One2many(comodel_name='hr.infraction', inverse_name='employee_id', string='Sanciones')
    
    #Prueba no incluide en Humanis
    #infraction_action_ids = fields.one2many('hr.infraction.action', 'employee_id', 'Acciones disciplinarias', readonly=True)
  