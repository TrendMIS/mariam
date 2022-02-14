# -*- coding: utf-8 -*-
{
    'name': "Trend Real Estate Design",
    'summary': "Add floor plans for buildings of project",
    'author': "Trend Development Team",
    'category': 'Sales',
    'depends': ['trend_realestate_project', 'trend_realestate_unit'],
    'data': [
        "views/design_building_view.xml",
        "views/design_plan_view.xml",
        "views/design_floor_view.xml",
        "views/building_template.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True,
    'auto_install': False,
    'sequence': 1
}
