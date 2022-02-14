# -*- coding: utf-8 -*-
{
    'name': "Trend Real Estate Installments Plan",
    'summary': "Trend Real Estate Installments Plan",
    'description': """
        This module calculate installments in quotations
          
     """,
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['account', 'trend_realestate_unit', 'trend_many2many_tags_link', 'trend_standard_payment_plan'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/sale_order_inherit_view.xml',
        'views/account_payment.xml',
        'wizard/payment_creation_wizard.xml',

    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
