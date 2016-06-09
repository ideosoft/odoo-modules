# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft ISP',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft ISP',
    'category': 'Contract Management',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft ISP Contract
==================================
        """,
    'data': [
        'views/contract.xml'
	],
     'depends': [
        'base', 'account_analytic_analysis'
     ],
    'installable': True,
    'application': False,
    'auto_install': False,
}