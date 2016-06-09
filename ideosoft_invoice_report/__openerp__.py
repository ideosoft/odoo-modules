# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft Invoice Report',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft Test Report',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo eFactura
==================================
        """,
    'data': [
        'views/report_style.xml',
		'views/report_invoice.xml',
	],
     'depends': [
        'account',
     ],
    'installable': True,
    'application': False,
    'auto_install': False,
}