# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Ddi(models.Model):
    '''Ddi'''
    
    _name = "pbx.ddi"
    _description = "DDI"
    
    _rec_name = 'number'

    def _search_inuse(self, operator, value):
        ids = set()

        if operator == '=' and value == True:    
            self.env.cr.execute("SELECT id FROM pbx_ddi WHERE number IN (SELECT exten FROM pbx_extension)")
        else:
            self.env.cr.execute("SELECT id FROM pbx_ddi WHERE number NOT IN (SELECT exten FROM pbx_extension)")
            
        res_ids = set(id[0] for id in self.env.cr.fetchall())
        ids = ids and (ids & res_ids) or res_ids
        if ids:
            return [('id', 'in', tuple(ids))]
        return [('id', '=', '0')]
        
    @api.multi
    def _compute_inuse(self):
        for record in self:
            found = self.env['pbx.extension'].search_count([('exten', '=', record.number)])
            record.inuse = found > 0

    number = fields.Char(string="Number", required=True)
    
    # country = fields.Many2one(comodel_name='res.country',string="Country")
    # state = fields.Many2one(comodel_name='res.country.state',string="State")
    # city = fields.Char(string="City")
    
    inuse = fields.Boolean(compute='_compute_inuse', string="In Use", search=_search_inuse)
    
    _sql_constraints = [
        ('number', 'unique(number)',
            'DDI Exists!'),
    ]