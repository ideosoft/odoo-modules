# -*- coding: utf-8 -*-

from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)
import calendar
import datetime

from openerp.tools import SUPERUSER_ID, DEFAULT_SERVER_DATE_FORMAT
import openerp.addons.decimal_precision as dp


LINE_TYPE_EXCEPTION = 'x'
LINE_TYPE_RECURRENT = 'r'
LINE_TYPE_ONETIME = 'o'


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def date_interval(start_date, month_end=True):
    if month_end:
        end_date = datetime.date(start_date.year,
                                 start_date.month,
                                 calendar.monthrange(start_date.year,
                                                     start_date.month)[1])
    else:
        end_date = add_months(start_date, 1) - datetime.timedelta(days=1)

    return start_date, end_date


def format_interval(start, end, date_format=DEFAULT_SERVER_DATE_FORMAT):
    return '(%s - %s)' % (start.strftime(date_format),
                          end.strftime(date_format))


def operation_date(date=None, context=None):
    if context is None:
        context = {}

    if date is None:
        date = context.get("operation_date", datetime.date.today())

    if not isinstance(date, datetime.date):
        date = datetime.datetime.strptime(
            date,
            DEFAULT_SERVER_DATE_FORMAT,
        ).date()

    return date

LINE_TYPE_EXCEPTION = 'x'
LINE_TYPE_RECURRENT = 'r'
LINE_TYPE_ONETIME = 'o'

L_S = ((LINE_TYPE_RECURRENT, 'Recurrent'),
         (LINE_TYPE_EXCEPTION, 'Exception'),
         (LINE_TYPE_ONETIME, 'One time'))

CONTRACT_SERVICE_STATES = [('draft', 'Waiting for activating'),
                               ('active', 'Active'),
                               ('inactive', 'Inactive')]

class contract_service(models.Model):

    _name = 'contract.service'

    @api.model
    def _default_price_unit(self):
        return 1.0

    @api.one
    @api.depends('price_unit', 'quantity', 'product_id')
    def _compute_price(self):
        self.price  = self.price_unit * self.quantity    
        
    activation_date = fields.Datetime('Activation date')
    billed_to_date = fields.Date('Billed until date')
    deactivation_date = fields.Datetime('Deactivation date')
    duration = fields.Integer('Duration')
    product_id = fields.Many2one(comodel_name='product.product', string='Product', required=True)
    
    
    category_id = fields.Many2one(comodel_name='product.category', string='Product Category')
    name = fields.Char('Description', size=64)
    analytic_line_type = fields.Selection(L_S,string='Type')

    require_activation = fields.Boolean('Require activation')
    account_id = fields.Many2one(comodel_name='account.analytic.account', string='Contract')
    
    quantity = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'),
        required=True, default=1)
        
    price_unit = fields.Float(string='Unit Price', required=True,
        digits=dp.get_precision('Product Price'),
        default=_default_price_unit)
    
    price = fields.Float(string='Amount', digits= dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_price')
        
    
    activation_line_generated = fields.Boolean('Activation Line Generated?')
    
    state = fields.Selection(selection=CONTRACT_SERVICE_STATES, string='State')
                              
    @api.model
    def create(self, values):
        if not values.get('require_activation'):
            values['state'] = 'active'
            values['activation_date'] = fields.Datetime.now()
            
        return super(contract_service, self).create(values)
        

    
    
    
    @api.multi
    def action_deactivate(self):        
        for obj in self:
            obj.state = 'inactive'
            obj.deactivation_date = fields.Datetime.now()

    @api.one
    def on_change_product_id(product_id):
        pass
            
    @api.one
    def on_change_qty(qty, price_unit):
        pass     
         
            
    @api.onchange('product_id')
    def _onchange_product_id(self):
        product = self.product_id

        if product:
            self.analytic_line_type = product.analytic_line_type
            self.require_activation = product.require_activation
            self.category_id = product.categ_id.id
            self.price_unit = product.lst_price
            
            if product.analytic_line_type == LINE_TYPE_RECURRENT:
                self.duration = 0
            else:
                self.duration = 1
        

    def _get_price(self):
        self.price = self.qty * self.price_unit

    def _get_product_price2(self):
    
        if self.product_id:
            self.price_unit = self.product_id.lst_price  
        else:
            self.price_unit = -1.0  
                              
    def _get_product_price(self, cr, uid, ids, field_name, arg, context=None):
        product_pricelist_obj = self.pool.get('product.pricelist')
        partner_id = self.browse(
            cr, uid, ids[0],
            context=context).account_id.partner_id.id
        pricelist_id = self.browse(
            cr, uid, ids[0],
            context=context
        ).account_id.partner_id.property_product_pricelist.id
        ret = {}
        for line in self.browse(cr, uid, ids, context=context):
            if line.product_id:
                ret[line.id] = product_pricelist_obj.price_get(
                    cr, uid, [pricelist_id],
                    line.product_id.id, 1, partner_id,
                    context=context)[pricelist_id]
            else:
                ret[line.id] = None

        return ret

    def _get_total_product_price(self, cr, uid, ids, field_name, arg,
                                 context=None):
        ret = {}
        for line in self.browse(cr, uid, ids, context=context):
            if line.qty:
                ret[line.id] = line.price_unit * line.qty
            else:
                ret[line.id] = None

        return ret



    _defaults = {
        'state':'draft',
        'activation_line_generated': False,
        'category_id': 1,
        'name':'',
        'qty':1
    }



        


    def _prorata_rate(self, days_used, days_in_month):
        """ Returns a rate to compute prorata invoices.
        Current method is days_used / days_in_month, rounded DOWN
        to 2 digits
        """
        return (100 * days_used // days_in_month) / 100.0

    def _get_prorata_interval_rate(self, cr, uid, change_date, context=None):
        """ Get the prorata interval and price rate.

        Returns a tuple (start_date, end_date, price percent)
        """
        month_days = calendar.monthrange(change_date.year,
                                         change_date.month)[1]
        start_date = add_months(change_date, 1)
        end_date = start_date.replace(day=month_days)
        used_days = month_days - change_date.day
        ptx = self._prorata_rate(used_days, month_days)

        return start_date, end_date, ptx

    def _get_prorata_interval_rate_deactivate(self, cr, uid, change_date,
                                              context=None):
        start_date, end_date, ptx = self._get_prorata_interval_rate(
            cr, uid, change_date, context=context)
        ptx = ptx * -1
        return start_date, end_date, ptx

    def _get_date_format(self, cr, uid, obj, context):
        partner_lang = obj.account_id.partner_id.lang
        res_lang_obj = self.pool['res.lang']
        query = [
            ('code', '=', partner_lang),
            ('active', '=', True)
        ]
        lang_id = res_lang_obj.search(cr, uid, query, context=context)
        if lang_id:
            date_format = res_lang_obj.browse(cr, uid,
                                              lang_id[0],
                                              context=context).date_format

        else:
            date_format = '%Y/%m/%d'
        return date_format

        
    @api.one
    def create_analytic_line(self, mode='manual'):
    
        print "*" * 80
        print "create_analytic_line " * 5
    
        ret = []
        record = {}
        
        account_analytic_line_obj = self.env['account.analytic.line']
        
        line = self
        interval = ''
        
        record = {
            'name': ' '.join([line.product_id.name, line.name or '', interval]),
            'amount': (line.price * -1),
            'account_id': line.account_id.id,
            'user_id': self.env.user.id,
            'general_account_id': line.product_id.property_account_expense.id,
            'product_id': line.product_id.id,
            'contract_service_id': line.id,
            'to_invoice': 1,
            'unit_amount': line.qty,
            'is_prorata': mode == 'prorata',
            'journal_id': 1
        }
        
        account_analytic_line_obj.create(record)
        
        line = self
        return
        

        date_format = self._get_date_format(cr, uid, line, context=context)
        start, end = None, None
        next_month = None

        amount = line.price

        if line.analytic_line_type == LINE_TYPE_RECURRENT:
            if mode == 'prorata':
                activation_date = date
                start, end, ptx = self._get_prorata_interval_rate(
                    cr, uid,
                    activation_date,
                    context=context,
                )

                amount = amount * ptx

            elif mode == 'cron':
                next_month = add_months(date, 1)
                next_month = datetime.date(
                    next_month.year,
                    next_month.month,
                    1)
                start, end = date_interval(next_month, False)

            elif mode == 'manual':
                start, end = date_interval(date, False)

            elif mode == 'subscription':
                line.write({'activation_line_generated': True})

        if start and end:
            interval = format_interval(start, end, date_format)
        else:
            interval = ''

        general_account_id = line.product_id.property_account_expense.id \
            or line.product_id.categ_id.property_account_expense_categ.id

        record = {
            'name': ' '.join([line.product_id.name,
                              line.name or '',
                              interval]),
            'amount': (amount * -1),
            'account_id': line.account_id.id,
            'user_id': uid,
            'general_account_id': general_account_id,
            'product_id': line.product_id.id,
            'contract_service_id': line.id,
            'to_invoice': 1,
            'unit_amount': line.qty,
            'is_prorata': mode == 'prorata',
            'date': (next_month or date).strftime(
                DEFAULT_SERVER_DATE_FORMAT),
            'journal_id': 1
        }

        if line.analytic_line_type == LINE_TYPE_EXCEPTION:
            new_duration = line.duration - 1
            line.write({'duration': new_duration})
            if new_duration <= 0:
                self.unlink(cr, SUPERUSER_ID, line.id)
                record['contract_service_id'] = False
        elif line.analytic_line_type == LINE_TYPE_ONETIME:
            if line.duration > 0:
                line.write({'duration': line.duration - 1})
            else:
                # Do not create an already billed line
                return 
                
        if 'default_type' in context:
            context.pop('default_type')

        ret.append(account_analytic_line_obj.create(cr, uid, record,
                                                    context))

        return ret

    def create_refund_line(self, cr, uid, ids,
                           mode='manual',
                           date=None,
                           context=None):
        context = context or {}
        date = operation_date(date, context)

        if type(ids) is int:
            ids = [ids]

        ret = []
        record = {}
        account_analytic_line_obj = self.pool.get('account.analytic.line')
        for line in self.browse(cr, uid, ids, context):
            if any((line.analytic_line_type != LINE_TYPE_RECURRENT,
                    mode != "prorata")):
                # Not handled for now, only pro-rata deactivate
                continue

            date_format = self._get_date_format(cr, uid, line, context=context)

            deactivation_date = date
            start, end, ptx = self._get_prorata_interval_rate_deactivate(
                cr, uid,
                deactivation_date,
                context=context,
            )

            amount = line.product_id.list_price * ptx

            interval = format_interval(start, end,
                                       date_format=date_format)

            general_account_id = (
                line.product_id.property_account_expense.id or
                line.product_id.categ_id.property_account_expense_categ.id
            )

            record = {
                'name': ' '.join([line.product_id.name,
                                  line.name or '',
                                  interval]),
                'amount': (amount * -1) * line.qty,
                'account_id': line.account_id.id,
                'user_id': uid,
                'general_account_id': general_account_id,
                'product_id': line.product_id.id,
                'contract_service_id': line.id,
                'to_invoice': 1,
                'unit_amount': line.qty,
                'is_prorata': mode == 'prorata',
                'date': date.strftime('%Y-%m-%d'),
                'journal_id': 1
            }

            if 'default_type' in context:
                context.pop('default_type')

            ret.append(account_analytic_line_obj.create(cr, uid, record,
                                                        context))
        return ret



