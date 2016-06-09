# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft Humanis SOLICITUDES',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft SOLICITUDES',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Humanis SOLICITUDES
===================================
        """,
    'data': [
		'views/solicitud_view.xml',
        'views/reports.xml',
        'res/hr.employee.tiposolicitud.csv'
	],
     'depends': [
		'hr',
		'ideosoft_humanis_base',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}