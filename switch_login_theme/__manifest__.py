# -*- coding: utf-8 -*-
{
    'name': 'Branded Login Theme & Customizer Studio',
    'version': '19.0.2.0.0',
    'category': 'Theme/Corporate',
    'summary': '100% Customizable Login Screen: Change Logo, Background Image, Gradient Colors, Card Style (Light/Dark/Glass), Layout & Texts from Settings',
    'description': '''
Branded Login Theme & Customizer Studio for Odoo 19
===================================================
Transform the default Odoo 19 login page into a fully customizable, modern corporate login experience — configured directly from Odoo UI with zero coding!

Key Features:
-------------
* **3 Layout Modes**: Split Screen (Left/Right), Split Screen Reversed, or Centered Card over Fullscreen Background.
* **3 Card Styles**: Clean Light Card, Modern Dark Mode Card, or Frosted Glassmorphism Card.
* **Custom Logo & Background Image**: Upload any custom login logo and any background image directly from Settings.
* **Color & Gradient Pickers**: Customize Primary Button Color, Background Gradient Colors, and Overlay Darkness.
* **Editable Texts & Footer**: Customize Welcome Subtitle, Hero Title, Tagline, Footer Text, and Database Manager link visibility.
* **One-Click Live Preview**: Preview your customized login page anytime directly from the studio.
    ''',
    'author': 'dnaj25',
    'website': 'https://github.com/dnaj25/odoo-addons',
    'license': 'LGPL-3',
    'depends': ['base', 'web'],
    'data': [
        'views/res_company_views.xml',
        'views/login_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'switch_login_theme/static/src/scss/login_theme.scss',
        ],
    },
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 29.0,
    'currency': 'EUR',
}