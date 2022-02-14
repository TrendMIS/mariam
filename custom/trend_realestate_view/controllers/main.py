# -*- coding: utf-8 -*-
from odoo import http


class RealStateReport(http.Controller):

    @http.route('/realstate_report/', auth='user', website=True)
    def realstate_report(self, **kw):
        for line in http.request.env['product.product'].search([]):
            print(line)
            print(line.categ_id)
            print(line.name)
        return http.request.render('trend_realestate_view.realstate_report', {
            'categories': http.request.env['product.category'].search([('product_count', '>', 0)]),
            'products': http.request.env['product.template'].search([]),
        })
