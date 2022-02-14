# -*- coding: utf-8 -*-
{
    'name': "Trend Real Estate Lead",
    'summary': "Trend Real Estate Lead",
    'description': """
        This module edit on crm module to add the following : \n
            1- Add new fields in lead like [Interested Units - Budget from and to - Area from and to - Last Comment - Unit Number - ...].\n
            2- Add new server action to assign salesperson for more than lead .\n
            3- Change lead team if user reassign sales person to different team .\n
            4- Change opportunity to lead in all screens.\n
            5- Change sales channel to sales  in all screens.\n
            6- Add new fields to campaign screen like [Budget - Date from - Date To - Number of assign leads].\n
            7- Add filter by mobile in lead screen.\n
            8- Add team leader in lead form and get it when mark lead as won.\n
            9- Add history in sales team.\n
            10- Add create invoice button in lead form if it marked as won.\n
            11- Edit on invoice report to add lead data.\n

     """,
    'author': "Trend Development Team",
    'depends': ['mail', 'crm', 'trend_realestate_project', 'sale_management', "trend_realestate_unit"],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_team_history_view.xml',
        'views/crm_team_inherit_view.xml',
        'views/sale_order_inherit_view.xml',
        'views/crm_lead_inherit_view.xml',
        'views/crm_stage_inherit_view.xml',
        'views/res_partner_inherit_view.xml',
        'views/utm_campaign_inherit_view.xml',
        'views/account_move_inherit_view.xml',
        'views/res_config_setting_inherit_view.xml',
        'views/mail_activity_inherit_view.xml',
        'views/product_inherit_view.xml',
        'views/status_type.xml',
        'wizard/assign_multi_lead_user_wizard_view.xml',
        'reports/account_invoice_report_inherit.xml',
        'views/menu_items_view.xml',
        'wizard/available_units_wizard.xml',
    ],

    "external_dependencies": {
        "python": ['html2text']
    },

    'installable': True,
    'auto_install': False,
    'sequence': 1
}
