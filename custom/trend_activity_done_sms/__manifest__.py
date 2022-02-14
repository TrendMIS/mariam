# -*- coding: utf-8 -*-
{
    'name': "Trend Activity Done SMS",
    'summary': "Send sms automatically after done activity",
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['sms'],
    'data': [
        'views/mail_activity.xml'
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
