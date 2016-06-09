# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft Humanis VACACIONES',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft VACACIONES',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Humanis VACACIONES
================================
        """,
    'data': [
		'views/vacations_view.xml',
        'views/reports.xml',
	],
     'depends': [
        'hr',
		'ideosoft_humanis_base',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}