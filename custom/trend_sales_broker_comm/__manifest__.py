# -*- coding: utf-8 -*-
{
    'name': "Trend Sales Broker Commission",
    'summary': "Trend Sales Broker Commission",
    'description': """
        This module edit on crm and sales module to add the following : \n
            1- Add new feature for broker and broker salesman commission

     """,
    'author': "Trend Development Team",
    'depends': ["trend_realestate_lead"],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/sales_views.xml',
        'views/broker_commission_program_views.xml',
        'views/sale_broker_commission.xml',

    ],

    'installable': True,
    'auto_install': False,
}
