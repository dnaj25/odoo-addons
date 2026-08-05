{
    'name': 'Vendor Auto Tax',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Automatically apply default purchase tax configured on vendor to Purchase Order lines.',
    'description': """
This module adds a default purchase tax field to res.partner (vendors).
When creating a Purchase Order Line, Odoo will automatically apply this tax if configured on the vendor.
    """,
    'author': 'dnaj25',
    'website': 'https://github.com/dnaj25/odoo-addons',
    'depends': ['purchase', 'account'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'price': 19.00,
    'currency': 'EUR',
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
