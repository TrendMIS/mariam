# -*- coding: utf-8 -*-
{
    'name': "Trend Visit Activity Attendees",
    'summary': "Add attendees for visit activity type",
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['mail'],
    'data': [
        'data/mail_activity_data.xml',
        'security/ir.model.access.csv',
        'views/mail_activity_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1,
    'qweb': [
        'static/src/xml/activity.xml'
    ]
}
