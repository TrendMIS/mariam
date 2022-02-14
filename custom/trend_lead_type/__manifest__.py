# -*- coding: utf-8 -*-
{
    'name': "Trend Lead Type",
    'summary': "Add types to lead",
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['crm', 'trend_realestate_access_rights'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
