# -*- coding: utf-8 -*-
{   'application': True,
    'author': 'dnaj25',
    'category': 'Accounting',
    'currency': 'EUR',
    'data': [   'security/ir.model.access.csv',
                'views/res_config_settings_views.xml',
                'wizard/gemini_chat_wizard_views.xml',
                'views/gemini_menus.xml'],
    'depends': ['base', 'mail'],
    'description': '\n'
                   'This module provides a secure way to save Google Gemini API keys in general settings.\n'
                   'It offers a reusable python service helper for AI completions and a global chat wizard helper.\n'
                   '    ',
    'images': ['static/description/banner.png'],
    'installable': True,
    'license': 'LGPL-3',
    'name': 'Odoo Gemini AI Integration',
    'price': 59.0,
    'summary': 'General integration module with Google Gemini AI to assist users across all Odoo modules.',
    'version': '1.0',
    'website': 'https://github.com/dnaj25/odoo-addons'}