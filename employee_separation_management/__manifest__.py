# -*- coding: utf-8 -*-
{   'application': True,
    'author': 'dnaj25',
    'auto_install': False,
    'category': 'Human Resources',
    'currency': 'EUR',
    'data': [   'security/ir.model.access.csv',
                'views/separation_views.xml',
                'report/separation_report.xml',
                'report/separation_report_template.xml'],
    'demo': [],
    'depends': ['hr', 'hr_holidays'],
    'description': '\n'
                   'Employee Separation & End of Service Management\n'
                   '===============================================\n'
                   'This module automates the employee separation and offboarding process:\n'
                   '* Tracks resignation and dismissal/termination requests.\n'
                   '* Auto-calculates End of Service Gratuity benefits based on labor law.\n'
                   '* Auto-calculates Leave Encashment value for remaining leave balance.\n'
                   '* Tracks final deductions like loan recovery and asset returns.\n'
                   '* Implements a multi-level approval workflow (HR Manager, Finance Manager).\n'
                   '* Generates a professional Final Settlement PDF report.\n'
                   '    ',
    'images': ['static/description/banner.png'],
    'installable': True,
    'license': 'LGPL-3',
    'name': 'Employee Separation & End of Service Management',
    'price': 49.0,
    'summary': 'Manage employee resignation, end of service benefits, gratuity, leave encashment, and final '
               'settlement.',
    'version': '19.0.1.0.0',
    'website': 'https://github.com/dnaj25/odoo-addons'}