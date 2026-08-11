# -*- coding: utf-8 -*-
{   'application': True,
    'author': 'dnaj25',
    'category': 'Accounting',
    'currency': 'EUR',
    'data': ['security/ir.model.access.csv', 'views/product_views.xml', 'views/res_config_settings_views.xml'],
    'depends': ['product', 'stock'],
    'description': '\n'
                   'This module allows users to configure unlimited extra barcodes per product.\n'
                   'It integrates searching by extra barcodes across sales, purchase, stock, and invoicing.\n'
                   'Includes inventory settings for unique barcode validation.\n'
                   '    ',
    'images': ['static/description/banner.png'],
    'installable': True,
    'license': 'LGPL-3',
    'name': 'Product Multi Barcode | Search Extra Barcodes',
    'price': 45.0,
    'summary': 'Add unlimited extra barcodes per product variant and search by any barcode in Sales, Purchase, Stock, '
               'Invoice.',
    'version': '1.0',
    'website': 'https://github.com/dnaj25/odoo-addons'}