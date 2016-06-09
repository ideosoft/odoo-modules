# -*- coding: utf-8 -*-
{
    'name' : 'Ideosoft Humanis TELEFONOS',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft TELEFONOS',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Humanis TELEFONOS
=================================
        """,
   'data': [
        'views/phone_view.xml',
    ],
    'depends': [
        'hr',
        'ideosoft_humanis_base',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,    
}