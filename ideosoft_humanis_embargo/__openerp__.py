# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft Humanis EMBARGOS',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft EMBARGOS',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Humanis EMBARGOS
================================
        """,
    'data': [
		'views/embargo_view.xml',
	],
     'depends': [
		'hr',
		'ideosoft_humanis_base',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}