{
    'name': 'Bank Counterparty Report',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Generate reports showing the counterparty account and partner for all bank receipts and payments.',
    'description': """
This module provides a detailed bank counterparty report.
It helps accountants track exactly where incoming money came from (source partner/account)
and where outgoing money went (destination partner/account) in real-time.
    """,
    'author': 'dnaj25',
    'website': 'https://github.com/dnaj25/odoo-addons',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/bank_counterparty_report_views.xml',
    ],
    'price': 29.00,
    'currency': 'EUR',
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
