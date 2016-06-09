# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft Humanis RECURSOS',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft RECURSOS',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Humanis RECURSOS
================================
        """,
    'data': [
		'views/recurso_view.xml',
        'res/hr.employee.tiporecurso.csv'
	],
     'depends': [
		'hr',
		'ideosoft_humanis_base',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}