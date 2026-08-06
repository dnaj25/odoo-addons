{
    'name': 'Recurring Payments & Entries',
    'category': 'Accounting',
    'version': '1.0.0',
    'description': """Odoo 19 Recurring Payment, Recurring Payment In Odoo, Odoo 19 Accounting""",
    'summary': 'Use recurring payments to handle periodically repeated payments',
    'sequence': 11,
    'depends': ['account'],
    'data': [
        'data/sequence.xml',
        'data/recurring_cron.xml',
        'security/ir.model.access.csv',
        'views/recurring_template_view.xml',
        'views/recurring_payment_view.xml'
    ],
    'author': 'dnaj25',
    'website': 'https://github.com/dnaj25/odoo-addons',
    'price': 29.00,
    'currency': 'EUR',
    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
}
