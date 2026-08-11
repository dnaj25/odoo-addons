# -*- coding: utf-8 -*-
{   'application': True,
    'assets': {   'web.assets_backend': [   'switch_ai_dashboard/static/src/scss/dashboard_styles.scss',
                                            'switch_ai_dashboard/static/src/js/dashboard_action.js',
                                            'switch_ai_dashboard/static/src/xml/dashboard_template.xml']},
    'author': 'dnaj25',
    'category': 'Productivity/AI',
    'currency': 'EUR',
    'data': ['security/ir.model.access.csv', 'views/dashboard_templates.xml'],
    'depends': ['base', 'web', 'mail', 'odoo_gemini'],
    'description': '\n'
                   'This module provides a beautiful, branded business intelligence dashboard inside Odoo.\n'
                   'It calculates key statistics from your sales, purchases, and invoices, and integrates\n'
                   'with Google Gemini AI to auto-generate written executive briefings and smart insights.\n'
                   '    ',
    'images': ['static/description/banner.png'],
    'installable': True,
    'license': 'LGPL-3',
    'name': 'Switch AI Dashboard Studio',
    'price': 79.0,
    'summary': 'Interactive Odoo Business Intelligence Dashboard powered by Google Gemini AI.',
    'version': '19.0.1.0.0',
    'website': 'https://github.com/dnaj25/odoo-addons'}