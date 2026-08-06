{
    'name': 'Fixed Assets Management for Community',
    'version': '1.0.0',
    'depends': ['account'],
    'description': """Manage assets owned by a company or a person. 
        Keeps track of depreciation's, and creates corresponding journal entries""",
    'summary': 'Odoo 19 Assets Management',
    'category': 'Accounting',
    'sequence': 10,
    'data': [
        'data/account_asset_data.xml',
        'security/account_asset_security.xml',
        'security/ir.model.access.csv',
        'wizard/asset_depreciation_confirmation_wizard_views.xml',
        'wizard/asset_modify_views.xml',
        'views/account_asset_views.xml',
        'views/account_move_views.xml',
        'views/account_asset_templates.xml',
        'views/asset_category_views.xml',
        'views/product_views.xml',
        'report/account_asset_report_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'community_accounting_asset/static/src/scss/account_asset.scss',
        ],
    },
    'author': 'dnaj25',
    'website': 'https://github.com/dnaj25/odoo-addons',
    'price': 29.00,
    'currency': 'EUR',
    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
}
