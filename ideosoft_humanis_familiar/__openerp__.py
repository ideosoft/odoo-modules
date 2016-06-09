# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft Humanis FAMILIARES',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft FAMILIARES',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Humanis FAMILIARES
==================================
        """,
    'data': [
		'views/family_view.xml',
	],
     'depends': [
		'hr',
		'ideosoft_humanis_base',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}