# -*- coding: utf-8 -*-
{
    'name': "Trend Edit Customer Lead Admin",
    'summary': "Allow sales admin only to edit lead customer",
    'author': "Trend Development Team",
    'category': 'crm',
    'depends': ['trend_realestate_access_rights'],
    'data': [
        'views/crm_lead_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
