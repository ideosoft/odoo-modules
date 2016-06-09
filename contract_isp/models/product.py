# -*- coding: utf-8 -*-

from openerp import models, fields

LINE_TYPE_RECURRENT = 'r'
LINE_TYPE_EXCEPTION = 'x'
LINE_TYPE_ONETIME = 'o'

class Product(models.Model):

    ANALYTIC_LINE_TYPES = [
            (LINE_TYPE_RECURRENT, 'Recurrent X'),
            (LINE_TYPE_EXCEPTION, 'Exception X'),
            (LINE_TYPE_ONETIME, 'One time X')
        ]

    _inherit = 'product.product'

    analytic_line_type = fields.Selection(selection=ANALYTIC_LINE_TYPES, string='Type in contract')
        
    require_activation = fields.Boolean(string='Require activation', default=False)
    
class ProductTemplate(models.Model):

    ANALYTIC_LINE_TYPES = [
            (LINE_TYPE_RECURRENT, 'Recurrent X'),
            (LINE_TYPE_EXCEPTION, 'Exception X'),
            (LINE_TYPE_ONETIME, 'One time X')
        ]

    _inherit = 'product.template'

    analytic_line_type = fields.Selection(selection=ANALYTIC_LINE_TYPES, string='Type in contract')
        
    require_activation = fields.Boolean(string='Require activation', default=False)