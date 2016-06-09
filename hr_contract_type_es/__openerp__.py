# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'Employee Contracts Spain',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """
Add all information on the employee form to manage contracts.
=============================================================

    """,
    'author': 'OpenERP SA',
    'website': 'https://www.odoo.com/page/employees',
    'depends': ['base_action_rule', 'hr'],
    'data': [
        'views/hr_contract_type_es.xml',
        'views/hr_contract_type.xml',
        'views/hr_contract.xml',

        'data/hr_contract_type_es.xml'
    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
