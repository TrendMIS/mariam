# -*- coding: utf-8 -*-
{
    'name': "Trend Activity Done Archive",
    'summary': "Archive done activities before deleting them",
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['mail', 'trend_realestate_access_rights'],
    'data': [
        'views/mail_activity_archive.xml',
        'security/activity_rules.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
