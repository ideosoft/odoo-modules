# -*- coding: utf-8 -*-

{
    'name' : 'Ideosoft Humanis CONVENIOS',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft CONVENIOS',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Módulo Humanis CONVENIOS
=================================
Incluye: 
		- Convenio
		- Festivo
		- Absentismo
		- (Seguramente) Vacaciones
        """,
    'data': [
		'views/convenio_view.xml',	
		'views/public_holiday_view.xml',
        'res/hr.employee.tipoabsentismo.csv',
        'res/hr.employee.convenio.csv',
        'res/res.public_holiday.csv'
        #'views/reports.xml'
	],
     'depends': [
		'hr',
		'ideosoft_humanis_base',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}