# -*- coding: utf-8 -*-
{
    'name': "Trend Real Estate Unit",
    'summary': "Trend Real Estate Unit",
    'description': """
        This module edit on product module to add the following : \n
            1- Change product to unit in all system.\n
            2- Add new fields in unit form like [Developer - Area - Meter Price - Net Area - Estimated Price - ..] .\n
   
     """,
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['crm', 'purchase', 'sale_management', 'trend_realestate_contact',
                'trend_realestate_access_rights'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/reserve_wizard_view.xml',
        'data/product_attribute_data_view.xml',
        'data/cron.xml',
        'views/product_category_inherit_view.xml',
        'views/product_inherit_view.xml',
        'views/sale_order_inherit_view.xml',
        'views/menu_items_view.xml',
    ],

    'installable': True,
    'auto_install': False,
    'sequence': 1,
    'assets': {
        'web.assets_backend': [
            'trend_realestate_unit/static/src/css/ribbon.css',
        ],
    },
}
