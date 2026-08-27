# -*- coding: utf-8 -*-
{   'application': True,
    'author': 'dnaj25',
    'category': 'Accounting',
    'currency': 'EUR',
    'data': ['security/ir.model.access.csv', 'views/bank_counterparty_report_views.xml'],
    'depends': ['account'],
    'description': '\n'
                   'This module provides a detailed bank counterparty report.\n'
                   'It helps accountants track exactly where incoming money came from (source partner/account)\n'
                   'and where outgoing money went (destination partner/account) in real-time.\n'
                   '    ',
    'images': ['static/description/banner.png'],
    'installable': True,
    'license': 'LGPL-3',
    'name': 'Bank Counterparty Report',
    'price': 29.0,
    'summary': 'Generate reports showing the counterparty account and partner for all bank receipts and payments.',
    'version': '1.0',
    'website': 'https://github.com/dnaj25/odoo-addons'}