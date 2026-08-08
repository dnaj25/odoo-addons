# -*- coding: utf-8 -*-
{
    'name': 'WhatsApp Web Integration',
    'summary': 'Send Sale Orders, Invoices, Purchase Orders and messages via WhatsApp Web',
    'description': """
WhatsApp Web Integration
========================
This module allows users to send predefined and custom messages to partners (customers/vendors) via WhatsApp Web.

Key Features:
-------------
* One-click redirection to WhatsApp Web with pre-filled message texts.
* Send messages from Contacts (res.partner).
* Send messages from Sales Orders (sale.order) with order reference, amount, and links.
* Send messages from Invoices (account.move) with invoice reference and amount.
* Send messages from Purchase Orders (purchase.order) to vendors.
* Interactive pop-up wizard to customize messages before sending.
* Simple setup using the browser's active WhatsApp session.
""",
    'author': 'dnaj25',
    'website': 'https://github.com/dnaj25/odoo-addons',
    'category': 'Sales/CRM',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['base', 'sale', 'account', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/whatsapp_wizard_views.xml',
        'views/partner_views.xml',
        'views/sale_views.xml',
        'views/invoice_views.xml',
        'views/purchase_views.xml',
    ],
    'price': 19.00,
    'currency': 'EUR',
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
