# -*- coding: utf-8 -*-

from openerp import models, fields, api, tools

SQL_CREATE_VIEW = """
CREATE OR REPLACE VIEW radippool AS (
    SELECT
        id,
        pool_name,
        framedipaddress,
        nasipaddress,
        calledstationid,
        callingstationid,
        expiry_time,
        username,
        pool_key
    FROM
        {}
    ORDER BY id
)
"""

class IPPool(models.Model):

    _name = "radius.ippool"
    _description = "IP Pool"
    _table = 'radippool'

    def init(self, cr):
        #tools.drop_view_if_exists(cr, 'radippool')
        #cr.execute(SQL_CREATE_VIEW.format(self._table))
        pass
    
    pool_name = fields.Char(string='Pool Name', size=64)
    framedipaddress = fields.Char()
    nasipaddress = fields.Char(size=16)
    pool_key = fields.Char(size=64)
    calledstationid = fields.Char(size=16)
    callingstationid = fields.Char(size=16)
    expiry_time = fields.Datetime()
    username = fields.Char()
    