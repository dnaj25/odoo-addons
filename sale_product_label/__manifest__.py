# -*- coding: utf-8 -*-
{
    'name': 'Sales Product Labels',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Print product barcode and price labels directly from Sales Orders or Quotations.',
    'description': """
Sales Product Labels
====================
This module enables printing of custom product price and barcode labels directly from Sales Orders or Quotations, with quantities automatically set from ordered lines.
""",
    'author': 'Custom Addons',
    'depends': ['sale', 'product'],
    'data': [
        'views/sale_order_views.xml',
        'wizard/product_label_layout_views.xml',
    ],
    'images': [
        'static/description/cover.jpg',
    ],
    'license': 'OPL-1',
    'price': 39.00,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
}
