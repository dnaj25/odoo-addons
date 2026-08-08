# -*- coding: utf-8 -*-
{
    'name': 'Odoo Mobile App Connector',
    'summary': 'Secure REST API connector and management tools for native Android & iOS mobile apps',
    'description': """
Odoo Mobile App Connector
=========================
This module exposes secure REST API endpoints for building native/hybrid Android and iOS mobile applications. It also provides layout configurations directly from Odoo backend.

Key Features:
-------------
* Exposes secure endpoints for User Authentication (Signup, Login, Profiles).
* Exposes endpoints for Product Catalog and Category search.
* Exposes Shopping Cart and Checkout (Place Order) endpoints.
* Admin controls for homepage banners and featured sliders.
* Fully compatible with standard Odoo checkout flow.
""",
    'author': 'dnaj25',
    'website': 'https://github.com/dnaj25/odoo-addons',
    'category': 'Mobile',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['base', 'website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/mobile_banner_views.xml',
    ],
    'price': 49.00,
    'currency': 'EUR',
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
