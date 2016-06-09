# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv

class animal(osv.Model):

    _name="animal.animal"
    _description="Pet Clinic"
    _columns={
        'code' : fields.char("Code", size=16,required=True),
        'name' : fields.char("Nombre", size=256,required=True),
        'raza' : fields.many2one('animal.razas', 'id_raza'),
        'edad' : fields.char("Edad", size=3,required=True),
        'tamanyo' : fields.selection((('G','Grande'),('M','Mediano'),('P','Pequeño')),required=True),
        'estado' : fields.selection((('s','Sano'),('ns','Enfermo')),required=True),
        'color': fields.char("Color", size=256,required=True),
        'genero': fields.selection((('M','Macho'),('H','Hembra')),required=True),
    }
    
    _default={
		'code' : '',
        'name' : '',
        'edad': '',
        'tamanyo': 'G',
        'estado': '',
        'color': '',
        'genero': 'M'
    }
