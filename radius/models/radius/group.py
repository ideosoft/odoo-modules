# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Group(models.Model):

    _name = "radius.group"
    _description = "Group"
    
    @api.one
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('groupname', 'ilike', u"{}_copy%".format(self.groupname))])
        if not copied_count:
            new_name = u"{}_copy".format(self.groupname)
        else:
            new_name = u"{}_copy_{}".format(self.groupname, copied_count)

        default['groupname'] = new_name
        return super(Group, self).copy(default)

    groupname = fields.Char(string='Groupname', size=64, required=True)
    
    _sql_constraints = [
        ('groupname_unique',
         'UNIQUE(groupname)',
         "The groupname must be unique"),
    ]
