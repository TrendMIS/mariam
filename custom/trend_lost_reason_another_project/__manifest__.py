# -*- coding: utf-8 -*-
{
    'name': "Trend Another project Lost Reason",
    'summary': "Add the name of the other project for lost reason",
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['crm', 'trend_realestate_project'],
    'data': [
        'data/crm_lost_reason.xml',
        'wizard/crm_lead_lost_views.xml',
        'views/crm_lead_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
