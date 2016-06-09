# -*- coding: utf-8 -*-

from openerp import models, fields, api

class GroupCheck(models.Model):

    _name = "radius.groupcheck"
    _description = "Group Check"
    _inherit = "radius.attribute"
    
    groupname = fields.Char(string='Groupname', size=64, related='group_id.groupname', store=True)
