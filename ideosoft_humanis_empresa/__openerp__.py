# -*- coding: utf-8 -*-
{
    'name' : 'Ideosoft Humanis EMPRESA',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft EMPRESA',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Humanis EMPRESA
===============================
        """,
   'data': [
		'views/empresa_view.xml',
	],
	 'depends': [
		'hr',
		'ideosoft_humanis_base',
    ],
    'installable': True,
	'application': False,
    'auto_install': False,    
}