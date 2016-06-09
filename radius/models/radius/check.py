# -*- coding: utf-8 -*-

from openerp import models, fields, api, tools

RADIUS_ATTRIBUTE_CHECK =[
    ('Cleartext-Password', 'Cleartext-Password'),
    ('Auth-Type', 'Auth-Type')
]

SQL_CREATE_VIEW = """
CREATE OR REPLACE VIEW radcheck AS (
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
)"""


class Check(models.Model):

    _name = "radius.check"
    _description = "check"    
    _inherit = "radius.attribute"

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'radcheck')
        cr.execute(SQL_CREATE_VIEW.format(self._table))
    
    def _compute_display_name(self):
        name = "%s" % (self.username)
        self.display_name = name
        
    username = fields.Char(string='Username', size=64, select=1)
    attribute = fields.Selection(RADIUS_ATTRIBUTE_CHECK, string='Attribute')       
