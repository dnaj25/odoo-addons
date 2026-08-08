# -*- coding: utf-8 -*-
{
    'name': 'Web Responsive Pro',
    'version': '19.0.1.0.0',
    'category': 'Themes/Backend',
    'summary': 'Adds advanced layout responsiveness to the Odoo backend interface.',
    'description': """
Web Responsive Pro
==================
This module provides a fully responsive layout for the Odoo Community backend interface:
* Sticky list view table headers.
* Sticky form view statusbars.
* Mobile-friendly forms and optimized inputs.
* Clean chatter side-by-side positioning on wide screens.
""",
    'author': 'Custom Addons',
    'depends': ['web'],
    'assets': {
        'web.assets_backend': [
            'web_responsive/static/src/scss/web_responsive.scss',
        ],
    },
    'images': [
        'static/description/cover.jpg',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}
