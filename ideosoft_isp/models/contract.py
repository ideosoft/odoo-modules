# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

CONTRACT_STATES = (
    ('draft', 'Esperando Activacion'),
    ('active', 'Activo'),
    ('inactive', 'Inactivo')
)

CONTRACT_TYPES = (
    ('r', 'Recurrente'),
    ('x', 'Excepcional'),
    ('o', 'Una vez')
)
   
class Contract(models.Model):
 
  
    @api.multi
    def create_analytic_line(self):
        account_analytic_line_obj = self.env['account.analytic.line']
        record = {
                'name': ' ',
                'amount': 10.0 * (-1),
                'account_id': 0,
                'user_id': 0,
                'general_account_id': 0,
                'product_id': 0,
                'contract_service_id': l0,
                'to_invoice': 1,
                'unit_amount': 1,
                'is_prorata': True,
                'date': fields.Datetime.now().strftime('%Y-%m-%d'),
                'journal_id': 1
            }
            
        account_analytic_line_obj.create(record)
 
    @api.model
    def create(self, values):

        if not values['require_activation']:
            values['state'] = 'active'
            values['activation_date'] = fields.Datetime.now()

        id = super(Contract, self).create(values)
        return id
    
    @api.multi
    def action_desactivate(self):
        self.state = 'inactive'
    
    @api.multi
    def action_activate(self):
        self.state = 'active'
    
    @api.multi
    def action_reactivate(self):
        self.state = 'active'
        
    @api.onchange('product_id') 
    def product_id_change(self):
        if self.product_id:
            self.analytic_line_type = self.product_id.analytic_line_type
            self.require_activation = self.product_id.require_activation
            self.category_id = self.product_id.categ_id.id
            self.price = self.product_id.list_price
            if self.product_id.analytic_line_type in ('r', 'o'):
                self.duration = 0
            else:
                self.duration = 1
  
    _name = 'contract.service'        
        
    name = fields.Char('Description', size=64)
    activation_date = fields.Datetime(string='Fecha Activacion')
    duration = fields.Integer(string='Duration')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    category_id = fields.Many2one('product.category', string='Product Category')
    price = fields.Float(default=0, string="Precio")

    analytic_line_type = fields.Selection(CONTRACT_TYPES, string='Type')
    require_activation = fields.Boolean(string='Require activation')
    account_id = fields.Many2one('account.analytic.account', string='Contract')

    activation_line_generated = fields.Boolean(string='Activation Line Generated?')
    state = fields.Selection(CONTRACT_STATES, string='Estado', default='draft')
    
    
class account_analytic_account(models.Model):

    _name = 'account.analytic.account'
    _inherit = 'account.analytic.account'
       
    contract_service_ids  = fields.One2many('contract.service','account_id','Services')
    use_contract_services = fields.Boolean('Contract services')
    state = fields.Selection(
        [('template', 'Template'),('draft', 'New'),('open', 'In Progress'),('pending', 'Suspended'),('close', 'Closed'),('cancelled', 'Cancelled')],
        string='Status', required=True, track_visibility='onchange')

class account_analytic_line(models.Model): 
    
    _name = "account.analytic.line"
    _inherit = "account.analytic.line"
    
    @api.multi
    def create_analytic_lines(self):
        pass

    contract_service_id = fields.Many2one('contract.service',string='Service')
    is_prorata = fields.Boolean(string='Prorata', default=False)

    
class product_product(models.Model): 

    _inherit = 'product.product'
    _name = 'product.product'
    
    analytic_line_type = fields.Selection(CONTRACT_TYPES,string='Tipo de Servicio')
    require_activation = fields.Boolean(String='Requiere activacion')
