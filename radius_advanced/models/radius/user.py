# -*- coding: utf-8 -*-

from openerp import models, fields, api
import string
import random
import pprint

PASS_GENERATOR = string.ascii_uppercase + string.ascii_lowercase + string.digits


class Check(models.Model):
    _inherit = 'radius.check'
    
    user_id = fields.Many2one(comodel_name='radius.user', string='User', ondelete='cascade')

class UserGroup(models.Model):
    _inherit = 'radius.usergroup'
    
    user_id = fields.Many2one(comodel_name='radius.user', string='User', ondelete='cascade')
    
    
class User(models.Model):

    _name = "radius.user"
    _description = "User"
    
    @api.model
    def create(self, vals):
        
        check_id = self.env['radius.check'].create({
            'username': vals['username'],
            'attribute': 'Cleartext-Password',
            'op': ':=',
            'value': vals['password']
        })
        
        vals['check_id'] = check_id._ids

        vals['usergroup_ids'] = [];

        for group_id in vals['groups'][0][2]:
            vals['usergroup_ids'].append([0,0, {
                'check_id': check_id._ids,
                'group_id': group_id,
            }])
            
        return super(User, self).create(vals)
        
    @api.multi
    def write(self, vals):
        for user in self:
            usergroup_tuple = []
            if vals.get('usergroup_ids'):
                pass
                
            if vals.get('groups'):
                new_group = vals['groups'][0][2]           
                cur_group = [usergroup.group_id.id for usergroup in user.usergroup_ids]
                
                cre_group = list(set(new_group) - set(cur_group))
                del_group = list(set(cur_group) - set(new_group))
                
                print "Grupos OLD %s" % str(cur_group)                
                print "Grupos NEX %s" % str(new_group)
                
                print "Grupos CRE %s" % str(cre_group)
                print "Grupos DEL %s" % str(del_group)
                
                next_usergroups = self.env['radius.usergroup'].search([('group_id','in',new_group),('user_id','=',user.id)])                
                to_replace = [ug.id for ug in next_usergroups]
                
                dele_usergroups = self.env['radius.usergroup'].search([('group_id','in',del_group),('user_id','=',user.id)])                
                to_delete  = [ug.id for ug in dele_usergroups]
                
                print "Usergroup REP %s" % str(to_replace)
                print "Usergroup DEL %s" % str(to_delete)
                
                
                #usergroup_tuple.append((6, 0, to_replace))
                #[usergroup_tuple.append((2,o)) for o in to_delete]
           
                if to_replace:
                    usergroup_tuple.append((6, 0, to_replace))
                
                for create in cre_group:
                    usergroup_tuple.append((0,0,{'check_id': user.check_id.id, 'group_id': create}))
                
                print str(usergroup_tuple)
                                
                user.usergroup_ids = usergroup_tuple
                
                r = super(User, self).write(vals)
            
                #self.env['radius.usergroup'].browse(to_delete).unlink()
            
            return

    @api.multi
    def unlink(self):
        # if self.user_id:
        #     self.user_id.unlink()
        return super(User, self).unlink()
        
    @api.onchange('username')
    def _generate_pass(self):
        if not self.password:
            self.password = ''.join(random.choice(PASS_GENERATOR) for i in range(8)) 
        
    check_id  = fields.Many2one(comodel_name='radius.check', string='Check', readonly=False)
    
    username = fields.Char(string='Username', related='check_id.username')
    password = fields.Char(string='Password', related='check_id.value')

    groups = fields.Many2many(comodel_name='radius.group')
    
    usergroup_ids = fields.One2many(comodel_name='radius.usergroup', inverse_name='user_id', readonly=True)