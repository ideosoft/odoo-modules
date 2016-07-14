# -*- coding: utf-8 -*-
from openerp import models, fields, api
import re

def snake(name):
    s = re.sub(r'[^\w\s]','', name)
    s = re.sub(r'\s+','_',s)
    return s.lower()
    
class CallRoute(models.Model):
    '''Context'''
    
    _name = "pbx.callroute"
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
        return super(CallRoute, self).create(vals)
        
    name = fields.Char(string="Nombre", size=50, required=True)
    pattern = fields.Char(string="Patron", size=50)
    
    @api.onchange('test')
    def test_change(self):
        result = self.test
        
        if self.prefix_append:
            result = "%s%s" % (self.prefix_append, result)
        if self.suffix_append:
            result = "%s%s" % (result, self.suffix_append)
    
        print result
        
        self.result = result
        
        
    name = fields.Char(string="Nombre", size=50, required=True)
    pattern = fields.Char(string="Patron", size=50)
    replace_rules = fields.Boolean()
    prefix_strip = fields.Char()
    prefix_append = fields.Char()
    suffix_strip = fields.Char()
    suffix_append = fields.Char()
    
    test = fields.Char()
    result = fields.Char()
    