# -*- coding: utf-8 -*-
{
    'name': "Trend Lead First Assignee",
    'summary': "Keep track of the first lead assignee",
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['crm', "trend_realestate_access_rights"],
    'data': [
        'views/res_partner_inherit_view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
