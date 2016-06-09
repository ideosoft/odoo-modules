# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Wizard(models.TransientModel):
    _name = 'ideosoft.wizard'

    attendee_ids = fields.Many2many('res.partner', string="Attendees")
