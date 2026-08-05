{
    'name': 'Product Multi Barcode | Search Extra Barcodes',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Add unlimited extra barcodes per product variant and search by any barcode in Sales, Purchase, Stock, Invoice.',
    'description': """
This module allows users to configure unlimited extra barcodes per product.
It integrates searching by extra barcodes across sales, purchase, stock, and invoicing.
Includes inventory settings for unique barcode validation.
    """,
    'author': 'dnaj25',
    'website': 'https://github.com/dnaj25/odoo-addons',
    'depends': ['product', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'price': 45.00,
    'currency': 'EUR',
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
