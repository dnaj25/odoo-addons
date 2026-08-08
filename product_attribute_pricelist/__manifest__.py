# -*- coding: utf-8 -*-
{
    'name': 'Pricelist on Product Attribute',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Apply pricelist rules directly on specific product template attributes (e.g. Size, Color).',
    'description': """
Pricelist on Product Attribute
==============================
This module allows users to configure pricing and discount rules for specific product template attributes, instead of manually specifying every individual variant.
""",
    'author': 'Custom Addons',
    'depends': ['product', 'sale'],
    'data': [
        'views/product_pricelist_item_views.xml',
    ],
    'images': [
        'static/description/cover.jpg',
    ],
    'license': 'OPL-1',
    'price': 99.00,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
}
