# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft Humanis SINDICATOS',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft SINDICATOS',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Humanis SINDICATOS
==================================
        """,
    'data': [
		'views/sindicato_view.xml',
	],
     'depends': [
		'hr',
		'ideosoft_humanis_base',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}