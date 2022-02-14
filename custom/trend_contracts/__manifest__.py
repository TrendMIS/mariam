# -*- coding: utf-8 -*-
{
    'name': "Trend Realestate Contracts",
    'summary': "Add contracts reports",
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['trend_realestate_lead', 'trend_realestate_unit_info', 'trend_sales_broker_comm', 'trend_lead_type',
                'trend_contact_nationality'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/contract_report_type_views.xml',
        'reports/report.xml',
        'reports/report_contract_template.xml',
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1,
    'assets': {
        'web.report_assets_common': [
            'trend_contracts/static/src/css/contract_report.css',
        ],
    }
}
