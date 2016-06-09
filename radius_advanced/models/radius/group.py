# -*- coding: utf-8 -*-

from openerp import models, fields, api


class GroupCheck(models.Model):
    _inherit = "radius.groupcheck"
    
    group_id = fields.Many2one('radius.group', string='Group', ondelete='cascade')
    groupname = fields.Char(string='Groupname', related='group_id.groupname', store=True)
    
class GroupReply(models.Model):
    _inherit = "radius.groupreply"
    
    group_id = fields.Many2one('radius.group', string='Group', ondelete='cascade')
    groupname = fields.Char(string='Groupname', related='group_id.groupname', store=True)
    
    
    
class Group(models.Model):

    _name = "radius.group"
    _description = "Group"
    _inherit = "radius.group"

    @api.onchange('name')
    def name_normalize(self):
        if self.name:
            self.groupname = self.name.lower().replace(" ", "_")
            
    @api.multi
    def write(self, vals):
        if('groupname' in vals):
            print "groupname changed!!!"
        
        return super(Group, self).write(vals)
        
        
    name = fields.Char(string='Name', size=64)
     
    groupcheck_ids = fields.One2many(comodel_name='radius.groupcheck', inverse_name='group_id')
    groupreply_ids = fields.One2many(comodel_name='radius.groupreply', inverse_name='group_id')
    