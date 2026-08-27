# -*- coding: utf-8 -*-
{   'application': True,
    'author': 'dnaj25',
    'category': 'Accounting',
    'currency': 'EUR',
    'data': ['views/res_partner_views.xml'],
    'depends': ['purchase', 'account'],
    'description': '\n'
                   'This module adds a default purchase tax field to res.partner (vendors).\n'
                   'When creating a Purchase Order Line, Odoo will automatically apply this tax if configured on the '
                   'vendor.\n'
                   '    ',
    'images': ['static/description/banner.png'],
    'installable': True,
    'license': 'LGPL-3',
    'name': 'Vendor Auto Tax',
    'price': 19.0,
    'summary': 'Automatically apply default purchase tax configured on vendor to Purchase Order lines.',
    'version': '1.0',
    'website': 'https://github.com/dnaj25/odoo-addons'}