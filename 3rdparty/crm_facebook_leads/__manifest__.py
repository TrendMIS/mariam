# -*- coding: utf-8 -*-
{
    'name': "CRM Facebook Lead Ads",

    'summary': """
        Sync Facebook Leads with Odoo CRM""",

    'description': """
    """,

    'author': "BADEP, Vauxoo",
    'website': "https://badep.ma, www.vauxoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Lead Automation',
    'version': '12.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['crm', 'trend_realestate_project'],
    'images': ['static/src/img/banner.png'],
    'license': 'AGPL-3',

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/crm_view.xml',
    ]
}
