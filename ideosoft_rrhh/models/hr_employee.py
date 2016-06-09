# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv
from datetime import date, datetime

class hr_employee(osv.osv):
    def onchange_birthday(self, cr, uid, ids, birthday, context=None):
        today = datetime.now()
        birth = datetime.strptime(str(birthday),"%Y-%m-%d")
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return {'value': {'age': age}}
        
    def calculate_age(self, cr, uid, ids, name, args, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            today = datetime.now()
            birth = datetime.strptime(record.birthday,"%Y-%m-%d")
            age = today.year - birth.year
            res.append((record.id, age))
        return res
        
    _inherit = 'hr.employee'
    _description = "Employee"
    
    _columns={
        'course_ids' : fields.many2many('hr.course','employee_course_rel','self_id','code','Cursos'),
        'age':  fields.function(calculate_age,string='Age',type="integer"), 
    }
