# -*- coding: utf-8 -*-
{
    'name': "Ideosoft Configuracion",

    'summary': """Adaptacion configuracio nde ideosoft""",

    'description': """
        Hace esto:
            - A
            - B
            - C
    """,

    'author': "Ideosoft",
    'website': "http://www.ideoosft.es",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Technical Settings',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'res/res.company.csv',
        'res/res.users.csv',
        'views/wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'ideosoft.xml'
    ],
}