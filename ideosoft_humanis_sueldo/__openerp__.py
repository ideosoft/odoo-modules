# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft Humanis SUELDOS',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft SUELDOS',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Humanis SUELDOS
===============================
        """,
    'data': [
		'views/sueldo_view.xml',
	],
     'depends': [
		'hr',
		'ideosoft_humanis_base',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}