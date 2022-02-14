# -*- coding: utf-8 -*-
{
    'name': "Trend Search by phone or mobile",
    'summary': "Seacrh by phone or mobile",
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['trend_realestate_contact', 'crm'],
    'data': [
        'views/res_partner_view.xml',
        'views/crm_lead_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
