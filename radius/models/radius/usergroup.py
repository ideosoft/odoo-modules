# -*- coding: utf-8 -*-

from openerp import models, fields, api, tools

SQL_CREATE_VIEW = """
CREATE OR REPLACE VIEW radusergroup AS (
    SELECT
        id,
        username,
        groupname,
        priority
    FROM
        {}
    WHERE
        active IS True
    ORDER BY id
)
"""


class UserGroup(models.Model):

    _name = "radius.usergroup"
    _description = "Usergroup"
    _rec_name = 'display_name'

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'radusergroup')
        cr.execute(SQL_CREATE_VIEW.format(self._table))
    
    def _compute_display_name(self):
        name = "%s (%s)" % (self.username, self.groupname)
        self.display_name = name
        
    username = fields.Char('Username')
    groupname = fields.Char('Groupname') 
    priority = fields.Integer('Priority', default=0)
    
    active = fields.Boolean('Active', default=True)
    
    display_name = fields.Char(string='Display Name', compute='_compute_display_name', readonly=True)