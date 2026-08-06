{
    'name': 'Employee Separation & End of Service Management',
    'version': '19.0.1.0.0',
    'summary': 'Manage employee resignation, end of service benefits, gratuity, leave encashment, and final settlement.',
    'description': """
Employee Separation & End of Service Management
===============================================
This module automates the employee separation and offboarding process:
* Tracks resignation and dismissal/termination requests.
* Auto-calculates End of Service Gratuity benefits based on labor law.
* Auto-calculates Leave Encashment value for remaining leave balance.
* Tracks final deductions like loan recovery and asset returns.
* Implements a multi-level approval workflow (HR Manager, Finance Manager).
* Generates a professional Final Settlement PDF report.
    """,
    'author': 'dnaj25',
    'website': 'https://github.com/dnaj25/odoo-addons',
    'category': 'Human Resources',
    'depends': ['hr', 'hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        'views/separation_views.xml',
        'report/separation_report.xml',
        'report/separation_report_template.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 49.00,
    'currency': 'EUR',
    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
}
