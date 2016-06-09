# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv
from datetime import date, datetime

class res_partner(osv.osv):
    _inherit = 'res.partner'
    _columns = {
        'trade': fields.char('Trade name', size=128, select=True), # Nombre Comercial del Partner
    }

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args=[]
        if not context:
            context={}

        partners = super(res_partner, self).name_search(cr, uid, name, args,
                                                    operator, context, limit)
        ids = [x[0] for x in partners]
        if name and len(ids) == 0:
            ids = self.search(cr, uid, [('trade', operator, name)] + args,
                                                limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)
      

    def vat_change(self, cr, uid, ids, value, context=None):
        result = super(res_partner,self).vat_change(cr, uid, ids, value, context = context)
        if value:
            result['value']['vat'] = value.upper()
        return result
        
    def check_vat(self, cr, uid, ids, context=None):
        return True