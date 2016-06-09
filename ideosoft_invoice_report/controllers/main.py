# -*- coding: utf-8 -*-

from openerp.addons.web.http import Controller, route, request
from openerp.addons.web.controllers.main import _serialize_exception
from openerp.osv import osv
from openerp.tools import html_escape


class JsonController(Controller):

    @route([
        '/ideosoft_migration_tools/invoice/<ids>',
    ], type='http', auth='user', website=True)
    def invoice_json(self, ids=None, converter=None, **data):

        o = request.env['account.invoice'].search([['id','=',ids]])
    
        import json
        import requests
        
        x = {
            "number": o.number,
            "date_invoice": o.date_invoice,
            "date_start": o.date_invoice,
            "date_end": o.date_invoice,
            
            "partner_id": {
                "name": o.partner_id.name,
                "vat": o.partner_id.vat,
                "street": o.partner_id.street,
                "zip": o.partner_id.zip,
                "city": o.partner_id.city,
                "state": o.partner_id.state_id.name,
                "phone": o.partner_id.phone,
            },
            "invoice_line": [],
        }
        
        for line in o.invoice_line:
            x['invoice_line'].append({"name": line.name, "price_unit": line.price_unit, "price_subtotal": line.price_subtotal})
        
        
        r = requests.post("http://gestion.airebullas.es/invoice/generar5.php", data=json.dumps(x))
      
        pdf = r.content
        
        print pdf 
        
        
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        return request.make_response(pdf, headers=pdfhttpheaders)