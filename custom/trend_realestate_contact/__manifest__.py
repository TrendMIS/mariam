# -*- coding: utf-8 -*-
{
    'name': "Trend Real Estate Contact",
    'summary': "Trend Real Estate Contact",
    'description': """
        This module edit on contact screen to add the following : \n
            1- Make mobile field required .\n
            2- Apply validation on mobile depend in field in general configuration on system .\n
            3- Add new page for personal info include [Birth Date - Gender - Educational Degree - ..] .\n
            4- Add field to know if this partner is developer or not .\n
            5- Add filter by mobile in contact screen.\n
            
     """,
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['base', 'base_setup', 'contacts'],
    'data': [
        'views/res_config_setting_inherit_view.xml',
        'views/res_partner_inherit_view.xml',
    ],

    'installable': True,
    'auto_install': False,
    'sequence': 1
}
