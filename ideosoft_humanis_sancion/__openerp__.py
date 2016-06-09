# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft Humanis SANCIONES',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft SANCIONES',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Humanis SANCIONES
=================================
        """,
    'data': [
		'views/infraction_view.xml',
        'res/hr.infraction.category.csv'
	],
     'depends': [
		'hr',
		'ideosoft_humanis_base',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}