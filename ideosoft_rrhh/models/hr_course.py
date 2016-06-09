# -*- encoding: utf-8 -*-

from openerp import models, fields, api

class Course(models.Model):

    _name="hr.course"
    _description="Course"
    
    code = fields.Char(string="Code", size=16, required=True)
    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    hours = fields.Char(string="Hours")
