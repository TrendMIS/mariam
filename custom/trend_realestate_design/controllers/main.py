# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class LeadWebsiteForm(http.Controller):
    @http.route('/realestate-design/<int:building_id>', type='http', auth="user", methods=['GET'])
    def show_building(self, building_id):
        building = self._get_building(building_id)
        context = {
            "building": building,
            "getattr": getattr
        }
        return request.render(
            template='trend_realestate_design.building_page',
            qcontext=context
        )

    def _get_building(self, building_id):
        return request.env['design.building'].browse(building_id)
