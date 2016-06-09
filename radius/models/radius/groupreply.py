# -*- coding: utf-8 -*-

from openerp import models, fields, api, tools

SQL_CREATE_VIEW = """
CREATE OR REPLACE VIEW radgroupreply AS (
    SELECT
        id,
        groupname,
        attribute,
        op,
        value
    FROM
        {}
    WHERE
        active IS True
    ORDER BY id
)
"""

class GroupReply(models.Model):

    _name = 'radius.groupreply'
    _description = "Group Reply"
    _inherit = 'radius.attribute'
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'radgroupreply')
        cr.execute(SQL_CREATE_VIEW.format(self._table))
    
    def _compute_display_name(self):
        name = "%s" % (self.groupname)
        self.display_name = name

    groupname = fields.Char(string='Groupname', size=64, store=True)
