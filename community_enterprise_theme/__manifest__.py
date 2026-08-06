# -*- coding: utf-8 -*-
{
    'name': 'Odoo Enterprise Theme for Community',
    'summary': 'Adopt the premium Odoo Enterprise style & colors on Odoo Community Edition',
    'description': """
Odoo Enterprise Theme for Community
===================================
Give your Odoo Community Edition a premium look and feel matching the official Odoo Enterprise Edition style.

Key Features:
-------------
* Modern Light Design: Crisp white backgrounds, subtle shadows and clean borders.
* Signature Purple Branding: Adopts the iconic Odoo Enterprise purple accent (#714B67) across buttons, active tabs, and navigation elements.
* Clean Layout Styling: Polished backend views (Form, Tree, Kanban, Control Panel).
* Responsive and Optimized: Seamless SCSS compile times and works with Odoo 19.0 Community Edition.
""",
    'author': 'dnaj25',
    'website': 'https://github.com/dnaj25/odoo-addons',
    'category': 'Themes/Backend',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['web'],
    'assets': {
        'web.assets_backend': [
            'community_enterprise_theme/static/src/scss/variables.scss',
            'community_enterprise_theme/static/src/scss/style.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
