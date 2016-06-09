# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft Humanis CALENDAR',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft HUMANIS',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Humanis CALENDAR
===============================
        """,
    'data': [
        'views/ideocalendar.xml',
	],
    'depends': [
        'hr',
		'ideosoft_humanis_base',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}