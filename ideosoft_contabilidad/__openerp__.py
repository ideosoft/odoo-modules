# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft CONTABILIDAD / FACTURACIÓN',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft Contabilidad / Facturación',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft PartnerAccount
==================================
        """,
    'data': [
        'views/account.xml',
        'views/account_invoice.xml',
        'views/company.xml',
        'views/partner.xml',
    ],
     'depends': [
        'base',
        'account',
        'account_accountant',
     ],
    'installable': True,
    'application': False,
    'auto_install': False,
}