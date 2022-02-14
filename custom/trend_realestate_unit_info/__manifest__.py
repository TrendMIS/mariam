# -*- coding: utf-8 -*-
{
    'name': "Trend Real Estate Unit",
    'summary': "Trend Real Estate Unit Info",
    'description': """
        This module edit on product module to add the following : \n
            1- Change product to unit in all system.\n
            2- Add new fields in unit form like [Developer - Area - Meter Price - Net Area - Estimated Price - ..] .\n
   
     """,
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['trend_realestate_project', 'trend_realestate_unit', 'trend_realestate_access_rights', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_inherit_view.xml',
        'views/realestate_views.xml',
        'views/menu_items_view.xml',
    ],

    'installable': True,
    'auto_install': False,
    'sequence': 1
}
