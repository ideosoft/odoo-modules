# -*- coding: utf-8 -*-

from openerp import models, fields, api


class hr_contract(models.Model):
    _inherit = 'hr.contract'

    type_es_id = fields.Many2one(comodel_name='hr.contract.type.es', string='Tipo S. S.')
    
    
    @api.onchange('type_id')
    def onchange_type_id(self):
        print "***** onchange *****"
        if self.type_id:
            if self.type_id.type_es_id:
                self.type_es_id = self.type_id.type_es_id.id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
