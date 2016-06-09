{
    'name' : 'Ideosoft Modulo RESIDUOS',
    'author': 'Ideosoft CB',
    'version': '1.0',
    'summary': 'Ideosoft RESIDUOS',
    'category': 'Tools',
    'complexity': 'medium',
    'website': 'https://www.ideosoft.es/',
    'description':
        """
Ideosoft Modulo Contenedores Residuos
=================

Contenedores Residuos

        """,
    'data': [
        'views/residuo.xml',
        'views/residuo_entrada.xml',
        'views/residuo_salida.xml',
        'views/residuo_obra.xml',
        'views/residuo_tiporesiduo.xml',
        'views/residuo_tipounidad.xml',
        'views/residuo_codigoler.xml',
        'views/reports.xml',
        'security/security_residuo.xml',
        'res/res.groups.csv',
        'res/residuo.codigoler.csv',
    ],
    'depends' : ["web"],
    'qweb': [
        'static/src/xml/*.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
