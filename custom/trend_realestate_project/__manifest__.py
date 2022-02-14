# -*- coding: utf-8 -*-
{
    'name': "Trend Real Estate Project",
    'summary': "Trend Real Estate Project",
    'description': """
        This module edit on crm module to add the following : \n
            1- Change lead description to select project in all lead forms.\n
            2- Add real estate project to product from.\n
            3- Add real estate project types screen.\n
            4- Add real estate facilities screen.\n
            5- Add developers screen.\n
            6- Add screen for real estate project contain [Name - Address- Developer - Images - Facilities - Region - Unit Types - Presentation ... ] .\n

     """,
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['base_geolocalize', 'trend_realestate_contact', 'crm', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_facility_view.xml',
        'views/real_estate_project_type_view.xml',
        'views/real_estate_project_view.xml',
        'views/real_estate_project_image_view.xml',
        'views/product_inherit_view.xml',
        'views/menu_items_view.xml',
    ],

    'installable': True,
    'auto_install': False,
    'sequence': 1
}
