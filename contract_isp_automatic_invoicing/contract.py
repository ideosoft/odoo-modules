# -*- coding: utf-8 -*-

##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import orm

from openerp.addons.contract_isp_invoice.invoice import (
    PROCESS_CRON,
)


class account_analytic_account(orm.Model):
    _inherit = 'account.analytic.account'

    def cron_contract_automatic_invoicing(self, cr, uid, ids=None,
                                          context=None):
        if context is None:
            context = {}

        #if not context.get('create_analytic_line_mode', False):
        #    context['create_analytic_line_mode'] = 'cron'

        query = [
            ('state', '=', 'open'),
            ('type', '=', 'contract')
        ]

        ids_to_invoice = self.search(cr, uid, query, context=context)

        for contract_id in ids_to_invoice:
            self.create_analytic_lines(cr, uid, [contract_id], context=context)
            self.create_invoice(cr, uid, contract_id, PROCESS_CRON, context=context)
            cr.commit()
