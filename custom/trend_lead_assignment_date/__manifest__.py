# -*- coding: utf-8 -*-
{
    'name': "Trend Lead Assignment Date",
    'summary': "Trend Lead Assignment Date",
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['crm', "trend_lead_first_assignee"],
    'data': [
        'views/crm_lead.xml',
        'views/res_users.xml'
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
