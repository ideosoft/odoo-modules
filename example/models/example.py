# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Example(models.Model):
    _name = 'example.example'

    name = fields.Char(string='Name', required=True)
    date = fields.Date(string='Date')
    molokay = fields.Boolean()
    description = fields.Text()