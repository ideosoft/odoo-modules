# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Profile(models.Model):

    _name = "radius.profile"
    _description = "Profile"
    
    name = fields.Char(string='Name')
    groups = fields.Many2many(comodel_name='radius.group', relation='profile_group', column1='profile_id', column2='group_id', string='Grupos')