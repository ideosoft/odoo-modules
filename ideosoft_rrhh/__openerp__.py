{
    'name' : 'Ideosoft Modulo RRHH',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft RRHH',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Modulo RRHH
=================

RRHH

        """,
    'data': [
        'views/hr_courses_view.xml',
        'views/hr_employee_view.xml'
    ],
    'depends' : ["web", "hr"],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
