# -*- coding: utf-8 -*-
{
    'name': "Trend Realestate Report",
    'summary': "This Module Allow you to view Realestate Available and Reserved",
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['base', 'website', 'trend_realestate_unit'],
    'data': [
        'security/ir.model.access.csv',
        'views/realestate_report_template.xml',
        'views/realestate_report_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'assets': {
        'web.assets_frontend': [
            'trend_realestate_view/static/src/css/realestate.css',
            'trend_realestate_view/static/src/js/realestate.js',
        ],
    },
}
