# -*- coding: utf-8 -*-

from openerp import models, fields, api


class hr_contract_type_es(models.Model):
    _name = 'hr.contract.type.es'
    _description = 'Contract Type ES'
    _order = 'code'
    
    @api.one
    @api.depends('code')
    def _compute_display_name(self):
        self.display_name = "%s - %s" % (self.code, self.name)

    @api.multi
    @api.depends('display_name')
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, '%s' % record.display_name))
        return result
        
    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name')
    
    display_name = fields.Char(string="Display Name", compute='_compute_display_name')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
