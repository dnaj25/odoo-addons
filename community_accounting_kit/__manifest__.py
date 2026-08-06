{
    'name': 'Odoo 19 Accounting Community Kit',
    'version': '1.0.3',
    'category': 'Accounting',
    'summary': 'Accounting Reports, Asset Management and Budget, Recurring Payments, '
               'Lock Dates, Fiscal Year, Accounting Dashboard, Financial Reports, '
               'Customer Follow up Management, Bank Statement Import',
    'description': 'Odoo 19 Financial Reports, Asset Management and '
                   'Budget, Financial Reports, Recurring Payments, '
                   'Bank Statement Import, Customer Follow Up Management,'
                   'Account Lock Date, Accounting Dashboard',
    'live_test_url': 'https://www.youtube.com/c/OdooMates',
    'sequence': '1',
    'sequence': '1',
    'maintainer': 'Odoo Mates, Walnut Software Solutions',
    'support': 'odoomates@gmail.com',
    'depends': [
        'community_pdf_reports',
        'community_accounting_asset',
        'community_accounting_budget',
        'community_accounting_fiscal_year',
        'community_accounting_recurring_payments',
        'community_accounting_daily_reports',
        'community_accounting_followup',
    ],
    'data': [
        'security/group.xml',
        'views/menu.xml',
        'views/settings.xml',
        'views/account_group.xml',
        'views/account_tag.xml',
        'views/res_partner.xml',
        'views/account_bank_statement.xml',
        'views/payment_method.xml',
        'views/reconciliation.xml',
        'views/account_journal.xml',
    ],
    'application': True,
    'author': 'dnaj25',
    'website': 'https://github.com/dnaj25/odoo-addons',
    'price': 99.00,
    'currency': 'EUR',
    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
}

