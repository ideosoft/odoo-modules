# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools.translate import _


ACCOUNT_STATE = [('template', 'Template'),
    ('draft', 'New'),
    ('open', 'In Progress'),
    ('pending', 'Suspended'),
    ('close', 'Closed'),
    ('cancelled', 'Cancelled')]

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    account_analytic_account_id = fields.Many2one(comodel_name='account.analytic.account', string='AAA')

class account_analytic_account(models.Model):
    _inherit = 'account.analytic.account'
    
    contract_service_ids = fields.One2many(comodel_name='contract.service', inverse_name='account_id', string='Services')                                   
    use_contract_services = fields.Boolean(string='Contract services', default=False)
    state = fields.Selection(selection=ACCOUNT_STATE, string='Status', required=True, track_visibility='onchange')
    invoice_ids = fields.One2many(comodel_name='account.invoice', inverse_name='account_analytic_account_id', string="Invoices")
    
    @api.model
    def create(self, values):
    
        print "*" * 80
        import pprint
        pprint.pprint(values)
        print "*" * 80
    
    
        if values.get('type') == 'contract' and values.get('use_contract_services'):
            values['name'] = values['code']
            partner = self.env['res.partner'].browse([values['partner_id']])
            values['parent_id'] = partner.partner_analytic_account_id.id
        
            print "*" * 80
            import pprint
            print partner
            print partner.partner_analytic_account_id
            print partner.partner_analytic_account_id.id
            pprint.pprint(values)
            print "*" * 80        
     
        return super(account_analytic_account, self).create(values)
        
    def _get_invoice_ids(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if ids:
            cr.execute("""
                SELECT account_analytic_id, array_agg(invoice_id)
                FROM account_invoice_line
                WHERE account_analytic_id IN %s
                GROUP BY account_analytic_id
                """, (tuple(ids), ))
            values = dict(cr.fetchall())

            for i in ids:
                res[i] = values.get(i, [])

        return res

    def _search_invoice_ids(self, cr, uid, obj, name, args, context):
        query, params = [], []
        for key, op, value in args:
            if key != "invoice_ids":
                continue
            if op in ("=", "in") and not value:
                query.append("agg.invoice_ids = ARRAY[NULL]::integer[]")
            elif op in ("!=", "not in") and not value:
                query.append("NOT agg.invoice_ids = ARRAY[NULL]::integer[]")
            elif op in ("=", "in", "!=", "not in") and value:
                if isinstance(value, (int, long)):
                    value = [value]
                query.append("{0} agg.invoice_ids && ARRAY[{1}]".format(
                    "NOT" if op in ("!=", "not in") else "",
                    ", ".join(["%s"] * len(value)),
                ))
                params.extend(value)
            else:
                continue

        if not query:
            return []

        else:
            cr.execute(
                """
                SELECT array_agg(agg.id) FROM (
                    SELECT aaa.id as id
                         , array_agg(ail.invoice_id) as invoice_ids
                    FROM account_analytic_account aaa
                    LEFT JOIN account_invoice_line ail
                    ON ail.account_analytic_id = aaa.id
                    GROUP BY aaa.id
                    ) agg
                WHERE {0}""".format(" AND ".join(query)),
                params,
            )

            ids = cr.fetchone()[0]
            return [('id', 'in', tuple(ids))]

    def create_analytic_lines(self, cr, uid, ids, context=None):
        mode = 'manual'
        if context and context.get('create_analytic_line_mode', False):
            mode = context.get('create_analytic_line_mode')

        contract_service_obj = self.pool.get('contract.service')
        query = [
            ('account_id', 'in', ids),
            ('state', '=', 'active'),
            ('analytic_line_type', 'in', (LINE_TYPE_RECURRENT,
                                          LINE_TYPE_ONETIME,
                                          LINE_TYPE_EXCEPTION))
        ]
        contract_service_ids = contract_service_obj.search(cr, uid,
                                                           query,
                                                           order='account_id',
                                                           context=context)

        if contract_service_ids:
            contract_service_obj.create_analytic_line(cr, uid,
                                                      contract_service_ids,
                                                      mode=mode,
                                                      context=context)

        return {}

    def create_refund_lines(self, cr, uid, ids, context=None):
        context = context or {}
        mode = context.get('create_analytic_line_mode', 'manual')

        contract_service_obj = self.pool["contract.service"]
        query = [
            ('account_id', 'in', ids),
            ('state', '=', 'inactive'),
            # only recurrent is handled in refund right now
            ('analytic_line_type', 'in', (LINE_TYPE_RECURRENT,)),
        ]
        contract_service_ids = contract_service_obj.search(cr, uid,
                                                           query,
                                                           order='account_id',
                                                           context=context)

        if contract_service_ids:
            contract_service_obj.create_refund_line(cr, uid,
                                                    contract_service_ids,
                                                    mode=mode,
                                                    context=context)

        return {}



    def on_change_partner_id(self, cr, uid, ids,
                             partner_id, name,
                             code=None, context=None):
        res = {}
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id,
                                                          context=context)
            if partner.user_id:
                res['manager_id'] = partner.user_id.id
            if not name:
                if code:
                    res['name'] = code
                else:
                    res['name'] = _('Contract: ') + partner.name
            # Use pricelist from customer
            res['pricelist_id'] = partner.property_product_pricelist.id

        return {'value': res}


