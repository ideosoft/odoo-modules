# -*- coding: utf-8 -*-

from openerp import models, fields, api

class StdExtension(models.Model):
    '''Extension'''

    _name = 'pbx.stdextension' 
    _description = "Standard Extension"
    
    @api.multi
    def unlink(self):
        for record in self:
            record.extension_id.unlink()
        return super(StdExtension, self).unlink()
        
    @api.model
    def create(self, vals):

        dial = self.env['pbx.sipaccount'].search([('id','=',vals['sipaccount_id'])])
        tech = dial[0].tech
    
        extension_id = self.env['pbx.extension'].create({
            'app': 'Macro',
            'context': 'local',
            'appdata': "stdexten,%s,%s" % (tech, vals['exten'])
        }).id
    
        vals['extension_id'] = extension_id

        return super(StdExtension, self).create(vals)
        
        
    @api.depends('timeout')
    def _compute_appdata(self):
        for record in self:
            record.appdata = "SIP/xxx,%d" % record.timeout
        
    context = fields.Char(string="Context", related='extension_id.context', readonly=True)
    exten = fields.Char(string="Exten", related='extension_id.exten')
    priority = fields.Integer(string="Priority", related='extension_id.priority', default=1)
    extension_id = fields.Many2one('pbx.extension', 'Extension', readonly=True)
    sipaccount_id = fields.Many2one('pbx.sipaccount', 'Account') 
