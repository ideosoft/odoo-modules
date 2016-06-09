# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft Humanis OBSERVACIONES',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft OBSERVACIONES',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Humanis PUESTOS
===============================
        """,
    'data': [
		'views/observacion_view.xml',
	],
     'depends': [
		'hr',
		'ideosoft_humanis_base',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}