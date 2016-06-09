# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime
   
    
class CodigoLER(models.Model):

    _name = 'residuo.codigoler'
    _description = 'Codigos CER/LER'
    _order = 'code'
       
    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s - %s" % (record.code, record.description)))
        return result
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('code', 'ilike', name)] + args, limit=limit)
        if not recs:
            recs = self.search([('description', operator, name)] + args, limit=limit)
        return recs.name_get()
        
    @api.one
    @api.depends('code')
    def _compute_group(self):
        code = self.code or ""
        if len(code) > 2:
            self.group = code[:2]
        else:
            self.group = ""
    
    @api.one
    @api.depends('code')
    def _compute_subgroup(self):
        code = self.code or ""
        if len(code) > 5:
            self.subgroup = code[:5]
        else:
            self.subgroup = ""
                
    @api.one 
    @api.depends('code')
    def _compute_dangerous(self):
        code = self.code or ""
        self.dangerous = code.endswith('*')
            
    @api.one
    def disable(self):
        self.active = False
        
    @api.one
    def enable(self):
        self.active = True
        
    code = fields.Char(string='Codigo', size=16, required=True, translate=True)
    description = fields.Text(string="Descripcion")
    dangerous = fields.Boolean(string="Peligroso", compute=_compute_dangerous, store=True)
    group = fields.Char(string="Grupo", compute=_compute_group, store=True)
    subgroup = fields.Char(string="Subrupo", compute=_compute_subgroup, store=True)
    active = fields.Boolean(default=True)