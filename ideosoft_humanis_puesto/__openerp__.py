# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft Humanis PUESTOS',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft PUESTOS',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Humanis PUESTOS
===============================
        """,
    'data': [
		'views/puesto_view.xml',
        'res/hr.employee.categoriapuesto.csv'
	],
     'depends': [
		'hr',
		'ideosoft_humanis_base',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}