# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft Humanis CONTRATO',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft CONTRATO',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Humanis CONTRATO
================================
        """,
    'data': [
		'views/contrato_view.xml',
        'res/hr.contract.type.csv',
        'res/ir.cron.csv'
	],
     'depends': [
		'hr',
		'hr_contract',
		'ideosoft_humanis_base',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}