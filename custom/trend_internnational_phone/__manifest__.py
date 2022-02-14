# -*- coding: utf-8 -*-
{
    'name': "Trend International Phone",
    'summary': "Add international phone field",
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['trend_realestate_contact', 'trend_realestate_lead'],
    'data': [
        'views/res_partner_inherit_view.xml',
        'views/crm_lead_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1,
}
