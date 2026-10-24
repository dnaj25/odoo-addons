# -*- coding: utf-8 -*-
{
    'name': 'Unified Login & Backend Theme Studio',
    'version': '19.0.4.0.0',
    'category': 'Theme/Corporate',
    'summary': 'All-in-One Login Screen & Inside Backend Customizer: Presets, Top Navbar, Home App Menu, Logo, Background, Gradient Colors & Interactive Controls',
    'description': '''
Unified Login & Backend Theme Studio for Odoo 19
================================================
Transform both the Odoo 19 Login Page AND the Inside Backend (Top Navbar, Home App Menu, App Icon Cards, and Primary Buttons/Tabs) from a single, easy-to-use Theme Studio with zero coding!

Key Features:
-------------
* **5 One-Click Unified Theme Presets**: Corporate Royal Purple, Midnight Cyber Dark, Emerald Finance, Minimalist Glass, and Sunset Warm — updates both Login & Inside Backend simultaneously!
* **Inside Backend & Home App Menu Customizer**:
  - Top Navbar Style (Brand Gradient, Solid Custom Color, or Midnight Dark).
  - Home App Menu Background (Match Login Screen Background, Brand Gradient, Clean Light Minimalist, or Midnight Cyber Dark).
  - App Icon Card Styles (Frosted Glassmorphism Tile, Elevated White Card, or Dark Slate Card with smooth hover lift).
  - Unified Primary Accent Color across all internal buttons, active tabs, badges, and Kanban cards.
* **3 Login Layout Modes**: Split Screen (Left/Right), Split Screen Reversed, or Centered Card over Fullscreen Background.
* **3 Login Card Styles**: Clean Light Card, Modern Dark Mode Card, or Frosted Glassmorphism Card.
* **Custom Logo & Background Image**: Upload any custom login logo and any background image directly from Settings.
* **Announcement / Maintenance Banner**: Display important notices or maintenance alerts at the top of the login card.
* **Interactive Login Controls**: Clean Password Eye icon, Remember My Email option, Quick Support/Website links, and Animated Floating Background Shapes.
    ''',
    'author': 'dnaj25',
    'website': 'https://github.com/dnaj25/odoo-addons',
    'license': 'LGPL-3',
    'depends': ['base', 'web'],
    'data': [
        'data/login_studio_data.xml',
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
    'price': 39.0,
    'currency': 'EUR',
}