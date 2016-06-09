# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft Humanis CURSOS',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft CURSOS',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Humanis CURSOS
==============================
        """,
    'data': [
		'views/curso_view.xml',
	],
     'depends': [
		'hr',
		'ideosoft_humanis_base',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}