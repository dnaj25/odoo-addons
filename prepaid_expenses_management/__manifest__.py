# -*- coding: utf-8 -*-
{
    'name': 'Prepaid Expenses & Rent Management (Auto Deduction & Expiry Alert)',
    'name_ar': 'إدارة المصروفات المدفوعة مقدماً والإيجارات (الخصم التلقائي وتنبيه التجديد)',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Manage prepaid expenses (Rent, Insurance, Subscriptions) with automatic periodic journal entry deduction and last-month renewal alerts',
    'summary_ar': 'إدارة المصروفات المدفوعة مقدماً كالإيجار والتأمين مع استقطاع آلي دوري وقيود يومية وتنبيهات بآخر شهر للتجديد',
    'description': '''
Prepaid Expenses & Rent Management for Odoo 19
===============================================
This module provides a complete, automated techno-functional solution for managing prepaid expenses, 
deferred charges, and recurring asset allocations such as office rents, warehouse leases, software subscriptions, 
insurance policies, and maintenance contracts.

Key Features:
-------------
* **Flexible Contracts**: Define prepaid expenses with start/end dates, total amounts, and accounting accounts.
* **Prepaid Expense Types**: Categorize expenses (Rent, Insurance, Software Subscriptions, Maintenance, Gov Fees).
* **Automatic Schedule Generation**: Instantly compute and generate recognition schedules (Monthly, Quarterly, Semi-Annually, Annually, or Custom).
* **Automated Accounting Deductions**: Automatically generate and post monthly journal entries (Debit Expense / Credit Prepaid Asset) via cron job or one-click action.
* **Smart Balances**: Live computation of Recognized Amount, Remaining Balance, and Installments Progress.
* **Last-Month Expiry & Renewal Alerts**: Automatically flags contracts entering their final month (or custom notice days), creates scheduled activities, and sends notifications to accountants.
* **One-Click Renewal**: Easily renew expiring contracts for a new period with pre-filled terms.
* **Analytic Accounting Support**: Distribute expenses across analytic accounts / cost centers.
* **Smart Dashboard & Reports**: Kanban, Tree, Form, Graph, and Pivot views for financial forecasting.
    ''',
    'author': 'dnaj25',
    'website': 'https://github.com/dnaj25/odoo-addons',
    'license': 'LGPL-3',
    'depends': ['base', 'account', 'mail', 'analytic'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/prepaid_expense_type_data.xml',
        'data/ir_cron_data.xml',
        'views/prepaid_expense_views.xml',
        'views/prepaid_expense_type_views.xml',
        'views/prepaid_expense_menus.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 49.0,
    'currency': 'USD',
}
