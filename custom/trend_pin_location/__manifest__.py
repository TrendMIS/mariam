# -*- coding: utf-8 -*-
{
    'name': "Trend Pin Location",
    'summary': """ Get The Pin Location Google Maps""",
    'author': "Trend Development Team",
    'category': 'Uncategorized',
    'version': '14.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm'],

    # always loaded
    'data': [
        'views/mail_activity_type.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'trend_pin_location/static/src/js/location.js',
        ],
    },
}
