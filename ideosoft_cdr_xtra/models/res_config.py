# -*- coding: utf-8 -*-
from openerp import models, fields, api
from ftplib import FTP

class Company(models.Model):

    _name = 'res.company'
    _inherit = 'res.company'
    
    cdr_hostname = fields.Char()
    cdr_username = fields.Char()
    cdr_password = fields.Char()


class CDRConfigSettings(models.TransientModel):

    _name = 'cdr.config.settings'
    _inherit = 'res.config.settings'
        
    def _get_default_company(self):
        return self.env.user.company_id or False
    
    @api.one
    @api.onchange('hostname','username','password')
    def _check_login(self):
        if self.hostname and self.username and self.password:
            ftp = FTP()
            try:
                ftp.connect(self.hostname)
                ftp.login(self.username, self.password)
                self.check = "Conected"
                return
            except:
                pass
            self.check = "Not conected"
        
    company_id = fields.Many2one(comodel_name='res.company', default=_get_default_company)
    hostname = fields.Char(related='company_id.cdr_hostname', string="Hostname")
    username = fields.Char(related='company_id.cdr_username', string="Username")
    password = fields.Char(related='company_id.cdr_password', string="Password")
    check = fields.Char(string="Status", readonly=True)
    
    