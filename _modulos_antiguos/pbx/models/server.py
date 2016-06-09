# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from Asterisk import Manager

class Server(models.Model):
    '''pbx server object, stores the parameters of the IPBXs'''
    
    _name = "pbx.server"
    _description = "pbx Servers"

    name = fields.Char(string='Server Name', size=50, required=True)
    active = fields.Boolean(string='Active', default=True, help="The active field allows you to hide the pbx")
    host = fields.Char(string='Host o IP address', size=50, required=True, help="IP address or DNS name of the pbx server.")
    port = fields.Integer(string='Port', required=True, default=5038, help="TCP port on which the Manager Interface listens. ")
    
    login = fields.Char('Login', size=30, required=True, help="Login")
    password = fields.Char('Password', size=30, required=True, help="Password")
    
    status = fields.Char(string="Estado", compute='check_status', store=False)
    
    @api.multi
    def check_status(self):
        try:
            manager = Manager.Manager(
                (self.host, self.port),
                    self.login,
                    self.password)
        except Exception, e:
            self.status = "Connection Test Failed! %s" % e
        finally:
            manager.Logoff()
        self.status = "Conectado!"