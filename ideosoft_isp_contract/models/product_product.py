# -*- coding: utf-8 -*-

from openerp import models, fields

LINE_TYPE_RECURRENT = 'r'
LINE_TYPE_EXCEPTION = 'x'
LINE_TYPE_ONETIME = 'o'

ANALYTIC_LINE_TYPES = [
        (LINE_TYPE_RECURRENT, 'Recurrent'),
        (LINE_TYPE_EXCEPTION, 'Exception'),
        (LINE_TYPE_ONETIME, 'One time')]

class product_product(models.Model):
    _inherit = 'product.product'

    analytic_line_type = fields.Selection(selection=ANALYTIC_LINE_TYPES, string='Type in contract')
    require_activation = fields.Boolean(string='Require activation', default=False)