# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Extension(models.Model):
    '''Extension'''
    
    _name = 'pbx.extension'
    _description = "Extension"
    
    def init(self, cr):
        # cr.execute("""DROP VIEW extension;""")
        cr.execute(""" CREATE OR REPLACE VIEW extension AS
            SELECT id, context, exten, priority, app, appdata
            FROM pbx_extension WHERE active = True;
            """)
    
    exten = fields.Char(string="Exten", default="", size=40)
    context = fields.Char(string="Context", default="", size=40)
    priority = fields.Integer(string="Priority", default=0)
    app = fields.Char(string="App", default="", size=40)
    appdata = fields.Char(string="Data", default="", size=256)

    active = fields.Boolean(default=True)

    @api.multi
    def name_get(self):
        result = []
        result.append((
            self.id,
            "[%s] exten = %s,%d,%s(%s)" % (self.context, self.exten, self.priority, self.app, self.appdata)))
        return result