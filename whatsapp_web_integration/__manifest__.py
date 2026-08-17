# -*- coding: utf-8 -*-
{   'application': True,
    'author': 'dnaj25',
    'auto_install': False,
    'category': 'Sales/CRM',
    'currency': 'EUR',
    'data': [   'security/ir.model.access.csv',
                'views/whatsapp_wizard_views.xml',
                'views/partner_views.xml',
                'views/sale_views.xml',
                'views/invoice_views.xml',
                'views/purchase_views.xml'],
    'depends': ['base', 'sale', 'account', 'purchase'],
    'description': '\n'
                   'WhatsApp Web Integration\n'
                   '========================\n'
                   'This module allows users to send predefined and custom messages to partners (customers/vendors) '
                   'via WhatsApp Web.\n'
                   '\n'
                   'Key Features:\n'
                   '-------------\n'
                   '* One-click redirection to WhatsApp Web with pre-filled message texts.\n'
                   '* Send messages from Contacts (res.partner).\n'
                   '* Send messages from Sales Orders (sale.order) with order reference, amount, and links.\n'
                   '* Send messages from Invoices (account.move) with invoice reference and amount.\n'
                   '* Send messages from Purchase Orders (purchase.order) to vendors.\n'
                   '* Interactive pop-up wizard to customize messages before sending.\n'
                   "* Simple setup using the browser's active WhatsApp session.\n",
    'images': ['static/description/banner.png'],
    'installable': True,
    'license': 'LGPL-3',
    'name': 'WhatsApp Web Integration',
    'price': 19.0,
    'summary': 'Send Sale Orders, Invoices, Purchase Orders and messages via WhatsApp Web',
    'version': '19.0.1.0.0',
    'website': 'https://github.com/dnaj25/odoo-addons'}