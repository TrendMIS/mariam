# -*- coding: utf-8 -*-
{
    'name': 'Trend Print Payment Plan',
    'summary': 'Print Payment Plan',
    'author': 'Trend Development Team',
    'data': [
        'report/payment_print.xml',
        'views/sale_order_inherit_view.xml'
    ],
    'depends': ['base', 'trend_realestate_instalments_plan'],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
