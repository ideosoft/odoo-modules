# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

class account_invoice(models.Model):
    _name = "account.invoice"
    _inherit = 'account.invoice'
    
    @api.multi
    def invoice_efactura(self):

        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        self.sent = True
        return self.env['report'].get_action(self, 'account.efactura')

