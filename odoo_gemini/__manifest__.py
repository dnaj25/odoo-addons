{
    'name': 'Odoo Gemini AI Integration',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'General integration module with Google Gemini AI to assist users across all Odoo modules.',
    'description': """
This module provides a secure way to save Google Gemini API keys in general settings.
It offers a reusable python service helper for AI completions and a global chat wizard helper.
    """,
    'author': 'dnaj25',
    'website': 'https://github.com/dnaj25/odoo-addons',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'wizard/gemini_chat_wizard_views.xml',
        'views/gemini_menus.xml',
    ],
    'price': 59.00,
    'currency': 'EUR',
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
