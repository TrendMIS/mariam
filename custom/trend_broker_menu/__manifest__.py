# -*- coding: utf-8 -*-
{
    'name': 'Trend Broker Menu',
    'summary': 'Special menu for listing brokers',
    'author': 'Trend Development Team',
    'data': [
        'views/crm_menus_view.xml',
        'security/ir_rule.xml'
    ],
    'depends': ['crm', 'trend_realestate_contact', 'trend_realestate_access_rights'],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
