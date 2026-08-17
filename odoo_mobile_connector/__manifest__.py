# -*- coding: utf-8 -*-
{   'application': True,
    'author': 'dnaj25',
    'auto_install': False,
    'category': 'Mobile',
    'currency': 'EUR',
    'data': ['security/ir.model.access.csv', 'views/mobile_banner_views.xml'],
    'depends': ['base', 'website_sale'],
    'description': '\n'
                   'Odoo Mobile App Connector\n'
                   '=========================\n'
                   'This module exposes secure REST API endpoints for building native/hybrid Android and iOS mobile '
                   'applications. It also provides layout configurations directly from Odoo backend.\n'
                   '\n'
                   'Key Features:\n'
                   '-------------\n'
                   '* Exposes secure endpoints for User Authentication (Signup, Login, Profiles).\n'
                   '* Exposes endpoints for Product Catalog and Category search.\n'
                   '* Exposes Shopping Cart and Checkout (Place Order) endpoints.\n'
                   '* Admin controls for homepage banners and featured sliders.\n'
                   '* Fully compatible with standard Odoo checkout flow.\n',
    'images': ['static/description/banner.png'],
    'installable': True,
    'license': 'LGPL-3',
    'name': 'Odoo Mobile App Connector',
    'price': 49.0,
    'summary': 'Secure REST API connector and management tools for native Android & iOS mobile apps',
    'version': '19.0.1.0.0',
    'website': 'https://github.com/dnaj25/odoo-addons'}