{
    'name': 'Print Journal Entries PDF Report',
    'version': '1.0',
    'summary': 'Print PDF voucher and report for Journal Entries',
    'category': 'Accounting/Accounting',
    'author': 'dnaj25',
    'depends': ['account'],
    'data': [
        'report/journal_entry_report.xml',
        'report/journal_entry_template.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
