# -*- coding: utf-8 -*-

from openerp import models, fields, api

class UserGroup(models.Model):

    _inherit = 'radius.usergroup'

    check_id = fields.Many2one('radius.check', string='Username')
    group_id = fields.Many2one('radius.group', string='Group')

    username = fields.Char('R. Username', related='user_id.username', store=True)
    groupname = fields.Char('R. Groupname', related='group_id.groupname', store=True) 