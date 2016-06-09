# -*- coding: utf-8 -*-

from openerp import models, fields, api

class sample(models.Model):
    _name = 'sample.sample'

    name = fields.Char()