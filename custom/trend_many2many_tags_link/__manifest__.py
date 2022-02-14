# -*- coding: utf-8 -*-
{
    'name': 'Trend Many2many Tags links',
    'summary': 'Open many2many tags form view',
    'author': 'Trend Development Team',
    'depends': ['web'],
    'installable': True,
    'auto_install': False,
    'sequence': 1,
    'assets': {
        'web.assets_backend': [
            'trend_many2many_tags_link/static/src/js/many2many_tags_link.js',
        ],
    },
}
