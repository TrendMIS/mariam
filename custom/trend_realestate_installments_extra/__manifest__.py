# -*- coding: utf-8 -*-
{
    'name': "Trend Real Estate Installments Extra",
    'summary': "Discounts, club, garage",
    'description': """
        This module adds discount on down payment and installments for garage and club
     """,
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['trend_realestate_instalments_plan'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_inherit_view.xml',
        'views/product_inherit_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
