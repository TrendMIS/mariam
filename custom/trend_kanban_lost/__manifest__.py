# -*- coding: utf-8 -*-
{
    'name': 'Trend Kanban lost',
    'summary': 'Open lost wizard when set record to lost in kanban',
    'author': 'Trend Development Team',
    'depends': ['web'],
    'installable': True,
    'auto_install': False,
    'sequence': 1,
    'assets': {
        'web.assets_backend': [
            'trend_kanban_lost/static/src/js/kanban_lost.js',
        ],
    },
}
