# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Reply(models.Model):

    _name = "radius.reply"
    _description = "Reply"
    _inherit = "radius.attribute"

  
    username = fields.Char('Username', size=64)

    
