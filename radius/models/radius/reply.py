# -*- coding: utf-8 -*-

from openerp import models, fields, api, tools

SQL_CREATE_VIEW = """
CREATE OR REPLACE VIEW radreply AS (
    SELECT
        id,
        username,
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

class Reply(models.Model):

    _name = "radius.reply"
    _description = "Reply"
    _inherit = "radius.attribute"

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'radreply')
        cr.execute(SQL_CREATE_VIEW.format(self._table))
    
    def _compute_display_name(self):
        name = "%s" % (self.username)
        self.display_name = name

    username = fields.Char('Username', size=64)
