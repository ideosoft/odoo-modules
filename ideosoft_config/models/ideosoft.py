# -*- coding: utf-8 -*-

from openerp import models, fields, api
from pprint import pprint

COUNTRY_SPAIN_DOMAIN = [('code', '=', 'ES')]

class IdeosoftTest(models.Model):
    _name = 'ideosoft.test'
    
    @api.one
    def ser_ideosoft(self):
        company = self.env['res.company'].browse(1)
        
        company.name = "Ideosoft C.B."
        
        company.street = "Periodista Leopoldo Ayuso, 5"
        company.street2 = "Bajo C"
        company.city = "Murcia"
        company.zip = "30009"
        
        company.country_id = self.env['res.country'].search(COUNTRY_SPAIN_DOMAIN)
        
        company.phone = "868183030"
        company.email = "administracion@ideosoft.es"

        company.rml_header1 = ""
        company.website = "http://www.ideosoft.es"
        
        
        admin = self.env['res.users'].browse(1)
        admin.in_group_8 = True
        
        
        return {}

    name = fields.Char()