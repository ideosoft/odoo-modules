# -*- coding: utf-8 -*-
{
    'name' : 'Ideosoft Humanis CITAS',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft CITAS',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Humanis CITAS
=============================
        """,
   'data': [
		'views/cita_view.xml',
	],
	 'depends': [
		'hr',
		'ideosoft_humanis_base',
    ],
    'installable': True,
	'application': False,
    'auto_install': False,    
}