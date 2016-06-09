# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft Radius ADV',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft Radius ADV',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Radius
==================================
        """,
    'data': [
        'views/menu.xml',
        
        'views/group.xml',
        'views/groupreply.xml',
        
        'views/usergroup.xml',
        
        
        'views/user.xml',
        #'views/profile.xml',

    ],
    'depends': ['radius'],
    'installable': True,
    'application': False,
    'auto_install': False,
}