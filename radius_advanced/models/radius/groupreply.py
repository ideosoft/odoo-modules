# -*- coding: utf-8 -*-

from openerp import models, fields, api

class GroupReply(models.Model):

    _name = "radius.groupreply"
    _description = "Group Reply"
    _inherit = "radius.attribute"

    groupname = fields.Char(string='Groupname', size=64, store=True)
