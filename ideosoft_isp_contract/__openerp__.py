# -*- coding: utf-8 -*-

{
    'name': 'Contract ISP',
    'version': '1.0',
    'category': 'Contract Management',
    'description': """
Manage service based contracts
==============================

This module adds a service based contract category were you can manage diferent
services and service types that are included in the contract.

Features:
---------

* Differents types of services (recurrent, exceptions, one time only),
* Pro-rata logic,
* Service activation wizard.
""",
    'author': "Savoir-faire Linux,Odoo Community Association (OCA)",
    'website': 'www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'depends': ['stock','account_analytic_analysis'],
    'data': [
            'security/contract_isp_security.xml',
            'security/ir.model.access.csv',
            'wizard/activate_contract_service.xml',
            'contract_isp_view.xml',
            'contract_isp_data.xml',
            'contract_isp_workflow.xml',
            'views/service.xml',
            'views/res_company.xml',
            'views/res_partner.xml',
            
            ],
    'active': False,
    'installable': True,
}
