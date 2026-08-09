# -*- coding: utf-8 -*-
{
    'name': 'Switch Fintech Login Theme',
    'summary': 'Custom beautiful login theme for Switch Fintech',
    'description': 'A premium, modern dark purple login screen customized for Switch Fintech.',
    'author': 'Dana Ajmi',
    'category': 'Theme/Corporate',
    'version': '19.0.1.0.0',
    'depends': ['web'],
    'data': [
        'views/login_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'switch_login_theme/static/src/scss/login_theme.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
