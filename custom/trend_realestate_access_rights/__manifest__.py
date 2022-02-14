# -*- coding: utf-8 -*-
{
    'name': "Trend Real Estate Access Rights",
    'summary': "Trend Real Estate Access Rights",
    'description': """
        This module add new category for real estate and four groups each group has access rights as following : \n
            1- Property Consultant [See his own customers and leads depend on assignation] .\n
            2- Sales Team Leader [See his own and his team customer and leads] .\n
            3- Sales Admin [See all leads and customers] .\n
            4- Operation Manager [See all leads and customers] .\n
            

            
     """,
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['crm', 'contacts', 'sales_team', 'sale_management'],
    'data': [
        'security/access_rights_security_view.xml',
        'security/ir.model.access.csv',
        'views/menu_item_view.xml',
    ],

    'installable': True,
    'auto_install': False,
    'sequence': 1
}
