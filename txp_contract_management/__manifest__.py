{
    'name': 'Contract Renewal & Expiry Management',
    'version': '1.0',
    'summary': 'Manage Employee, Vendor, Lease Contracts and Expiry Alerts',
    'category': 'Management',
    'author': 'dnaj25',
    'depends': ['base', 'mail', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'data/contract_cron.xml',
        'views/contract_type_views.xml',
        'views/contract_contract_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
