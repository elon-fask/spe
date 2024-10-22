# By Atman Boulaajaili
# https://github.com/elon-fask

{
    'name': 'Application Management',
    'version': '18.0.1.0',
    'author': 'Atman Boulaajaili',
    'category': 'Education',
    'description': 'Custom Application Management Module for California Crane School',
    "license": "LGPL-3",
    "website": "https://github.com/elon-fask/",
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/application_view.xml',
        "menu/application_menu.xml",
    ],
    'images': ["static/description/icon-crane.png"],
    'installable': True,
    'auto_install': False,
    'application': True,
}