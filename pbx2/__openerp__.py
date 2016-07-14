# -*- coding: utf-8 -*-
{
    'name': "pbx",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Ideosoft",
    'website': "http://www.ideosodt.es",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/menu.xml',
        'views/server.xml',
        'views/sipaccount.xml',
        'views/provision/menu.xml',
        'views/telephony/menu.xml',
        'views/telephony/ivrmenu.xml',
        
        
        
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}