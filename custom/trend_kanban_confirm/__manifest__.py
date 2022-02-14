# -*- coding: utf-8 -*-
{
    'name': 'Trend Kanban Confirm',
    'summary': 'Open confirm message when set record to lost or won in kanban',
    'author': 'Trend Development Team',
    'data': [
        'views/crm_lead_view.xml'
    ],
    'depends': ['web', 'crm'],
    'installable': True,
    'auto_install': False,
    'sequence': 1,
    'assets': {
        'web.assets_backend': [
            'trend_kanban_confirm/static/src/js/kanban_confirm.js',
        ],
    },
}
