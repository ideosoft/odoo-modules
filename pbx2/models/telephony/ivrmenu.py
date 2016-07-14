# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Entry(models.Model):
    '''IVR menu entry'''
    
    _name = 'telephony.ivrmenu.entry'
    _description = "IVR menu entry"
    _order = 'position'
    
    @api.one
    @api.onchange('ivrmenu_id')
    def ivrmenu_change(self):
        print "*** %s ***" % str(self.ivrmenu_id.id)
        self.position = self.env['telephony.ivrmenu.entry'].search_count([('ivrmenu_id','=',self.ivrmenu_id.id)])
    
    def compute_default_position(self):
        print "*** %s ***" % str(self.ivrmenu_id.id)
        c = self.env['telephony.ivrmenu.entry'].search_count([('ivrmenu_id','=',self.ivrmenu_id.id)])
        return c
    
    position = fields.Integer(string="Position", default=compute_default_position)
    action = fields.Char(string="Action")
    
    ivrmenu_id = fields.Many2one(comodel_name='telephony.ivrmenu', string="IVR Menu")
    
    _sql_constraints = [
        ('position_ivrmenu_unique', 'unique (position, ivrmenu_id)', 'Unique unique')
    ]
    
class IVRMenu(models.Model):
    '''IVR Menu'''
    
    _name = 'telephony.ivrmenu'
    _description = "IVR Menu"
    
    name = fields.Char(string="Name", required=True, ondelete='cascade', _help="The name of the menu")
    entry_ids = fields.One2many(comodel_name='telephony.ivrmenu.entry', inverse_name='ivrmenu_id', string="Entries")