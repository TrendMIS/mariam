{
    'name': "Trend Print Cheques",
    'author': "Trend Development Team",
    'depends': ['base', 'account', 'check_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/cheque_configuration_views.xml',
        'views/normal_payment_views.xml',
        'report/cheque_report.xml',

    ],
}
