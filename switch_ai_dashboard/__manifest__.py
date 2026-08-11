# -*- coding: utf-8 -*-
{
    'name': 'Switch AI Dashboard Studio',
    'version': '19.0.1.0.0',
    'category': 'Productivity/AI',
    'summary': 'Interactive Odoo Business Intelligence Dashboard powered by Google Gemini AI.',
    'description': """
This module provides a beautiful, branded business intelligence dashboard inside Odoo.
It calculates key statistics from your sales, purchases, and invoices, and integrates
with Google Gemini AI to auto-generate written executive briefings and smart insights.
    """,
    'author': 'Dana Ajmi',
    'website': 'https://github.com/dnaj25/odoo-addons',
    'depends': ['base', 'web', 'mail', 'odoo_gemini'],
    'data': [
        'security/ir.model.access.csv',
        'views/dashboard_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'switch_ai_dashboard/static/src/scss/dashboard_styles.scss',
            'switch_ai_dashboard/static/src/js/dashboard_action.js',
            'switch_ai_dashboard/static/src/xml/dashboard_template.xml',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
