# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

class TestReport(models.AbstractModel):
    _name = 'account.test_report'
    
    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('account.test_report')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
        }
        return report_obj.render('account.test_report', docargs)