# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft Humanis GENERAL',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft HUMANIS',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Humanis GENERAL
===============================
        """,
    'data': [
        'views/employee_view.xml',
	],
     'depends': [
        'base',
		'web',
        'base_iban',
        'es_bank_helper',
        'account_banking_sepa_credit_transfer',
        #'account_banking_sepa_direct_debit',
        'document',
        'ideosoft_humanis_base',
        'ideosoft_humanis_calendar',
		'ideosoft_humanis_cita',
		'ideosoft_humanis_contrato',
		'ideosoft_humanis_convenio',
		'ideosoft_humanis_curso',
		'ideosoft_humanis_embargo',
        'ideosoft_humanis_empleado',
        'ideosoft_humanis_empresa',
		'ideosoft_humanis_experiencia',
		'ideosoft_humanis_familiar',
        'ideosoft_humanis_hr_employee_partner',
		'ideosoft_humanis_observacion',
		'ideosoft_humanis_puesto',
		'ideosoft_humanis_recurso',
		'ideosoft_humanis_sancion',
		'ideosoft_humanis_sindicato',
		'ideosoft_humanis_solicitud',
		'ideosoft_humanis_sueldo',
        'ideosoft_humanis_telefono',
        'ideosoft_humanis_vacaciones',
    ],
    'css': [
        'static/src/css/custom.css'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}