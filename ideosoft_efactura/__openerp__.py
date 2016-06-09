# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft eFactura',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft eFactura',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo eFactura
==================================
        """,
    'data': [
		'views/efactura_view.xml',
	],
     'depends': [
        'account',
     ],
    'installable': True,
    'application': False,
    'auto_install': False,
}