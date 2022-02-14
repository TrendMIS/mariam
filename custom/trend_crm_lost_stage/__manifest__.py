# -*- coding: utf-8 -*-
{
    'name': "Trend Crm lost stage",
    'summary': "Add lost stage for crm that leads are being assigned to when marked lost",
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['crm'],
    'data': [
        'views/crm_stage_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
