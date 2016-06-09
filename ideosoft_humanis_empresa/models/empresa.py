# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date, datetime

PREPOSICIONES = [(' De', ' de'), (' Y', ' y'), (' En', ' en'), (' Al', ' al')]

def preposicion(string):
    
    for k, v in PREPOSICIONES:
        string = string.replace(k, v)
    return string
    

class Empresa(models.Model):

    _name = 'res.company'
    _inherit = 'res.company'
    _description = 'Empresa'
    
    cod_asesoria = fields.Char(string="Código asesoría")
    nif = fields.Char(string="NIF/CIF", size=9)
    nif_no_oblig = fields.Boolean(string="NIF no obligatorio")
    com_autonoma = fields.Char(string="Comunidad autónoma")
    tel2 = fields.Char(string="Teléfono 2")
    observaciones = fields.Text(string="Observaciones")
    
	
class Employee(models.Model):

    _name = 'hr.employee'
    _inherit = 'hr.employee'
    
    company_id = fields.Many2one(comodel_name='res.company', string='Empresa', ondelete='set null')
    area_id = fields.Many2one(comodel_name='res.company.area', string='Area', ondelete='set null')
    servicio_id = fields.Many2one(comodel_name='res.company.area.servicio', string='Servicio', ondelete='set null')
    centrotrabajo_id = fields.Many2one(comodel_name='res.company.area.servicio.centrotrabajo', string='Centro Trabajo', ondelete='set null')

    
class Area(models.Model):

    _name = 'res.company.area'
    _description = 'Area Regional'
    
    name = fields.Char(string="Área")
    ccc = fields.Char(string="CCC Patronal")
    empresa_id = fields.Many2one('res.company', string='Empresa', ondelete='cascade')
       
    
class Servicio(models.Model):

    _name = 'res.company.area.servicio'
    _description = 'Servicio'
    
    name = fields.Char(string="Servicio")
    empresa_id = fields.Many2one('res.company', string='Empresa', ondelete='cascade')
    area_id = fields.Many2one('res.company.area', string='Área', ondelete='cascade')
   
    
class CentroTrabajo(models.Model):

    _name = 'res.company.area.servicio.centrotrabajo'
    
    name = fields.Char(string="Nombre")
    #servicio_id = fields.Many2one('res.company.area.servicio', string='Servicio', ondelete='cascade')
    
    
    @api.model
    def create(self, values):
        
        values['name'] = preposicion(values['name'].title())
        id = super(CentroTrabajo, self).create(values)
        return id