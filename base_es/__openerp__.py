# -*- coding: utf-8 -*-
{
    'name' : 'Base ES',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Base ES',
    'description': """
The kernel of OpenERP, needed for all installation.
===================================================
""",
    'data': [
        'res/res.country.state.csv',
    ],
    'depends' : ["web"],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
}
