# -*- coding: utf-8 -*-
from openerp import models, fields, api
import re

def snake(name):
    s = re.sub(r'[^\w\s]','', name)
    s = re.sub(r'\s+','_',s)
    return s.lower()
    
class CallRule(models.Model):
    '''Context'''
    
    _name = "pbx.callrule"
    _description = "Call Route"
    
    @api.multi
    def unlink(self):
        for record in self:
            record.extension_id.unlink()
        return super(CallRule, self).unlink()
        
        
    @api.model
    def write(self, vals):
        if name in vals.keys():
            self.extension_id.write({'context': snake(vals['name'])})

        return super(CallRule, self).write(vals)
        
        
    @api.model
    def create(self, vals):

        extension_id = self.env['pbx.extension'].create({
            'app': 'Macro',
            'context': 'callrule-%s' % snake(vals['name']),
            'appdata': "dialtrunk,%s,${EXTEN}" % 'trunk'
        }).id
    
        vals['extension_id'] = extension_id

        return super(CallRule, self).create(vals)
        
    extension_id = fields.Many2one('pbx.extension', 'Extension', readonly=True)

    name = fields.Char(string='Callroute', size=50, required=True)
    
    context = fields.Char(string="Context", related='extension_id.context', readonly=True)
    exten = fields.Char(string="Exten", related='extension_id.exten')
