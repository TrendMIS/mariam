# -*- coding: utf-8 -*-
{
    'name': "Trend Mail Activity Reminder",
    'summary': "Mail Activity Reminder",
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['calendar', 'mail'],
    'data': [
       'data/calendar_alarm_data.xml',
       'views/mail_activity_inherit_view.xml'
    ],

    'installable': True,
    'auto_install': False,
    'sequence': 1
}
