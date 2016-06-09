# -*- coding: utf-8 -*-

from openerp import models, fields, api

class bufanda1(models.Model):
    _name = 'bufanda1.bufanda1'

    name = fields.Char()
    date = fields.Date()
    notes = fields.Char()
    active = fields.Boolean()