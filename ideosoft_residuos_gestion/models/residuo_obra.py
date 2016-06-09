# -*- encoding: utf-8 -*-

from openerp import models, fields, api

class Obra(models.Model):

    _name="residuo.obra"
    _description="Obra"
        
    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s - %s" % (record.code, record.name)))
        return result
        
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('code', 'ilike', name)] + args, limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()
        
    code = fields.Char(string="Código", size=8, required=True)
    name = fields.Char(string="Nombre", required=True)
    
    _sql_constraints = [
        ('code', 'unique(code)', 'code must be unique!'),
    ]