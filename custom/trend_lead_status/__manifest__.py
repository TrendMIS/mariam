# -*- coding: utf-8 -*-
{
    'name': "Trend Status Domain",
    'summary': "Add Domain to Status in lead depend on Stage",
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['trend_realestate_lead'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/change_stage.xml',
        'views/crm_stage_view.xml',
        'views/crm_lead_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
