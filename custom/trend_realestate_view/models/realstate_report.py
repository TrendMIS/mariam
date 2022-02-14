# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class RealstateReport(models.Model):
    _name = "product.realstate.report"
    _auto = False

    id = fields.Integer(string='id')
    name = fields.Char(string="Name", required=False, )
    product_category = fields.Char(string="Product Category", required=False, )
    qty = fields.Integer(string='Qty')

    def init(self):
        """ Event Question main report """
        tools.drop_view_if_exists(self._cr, 'product_realstate_report')
        self._cr.execute(

            """
                CREATE OR REPLACE VIEW product_realstate_report AS (
                SELECT
                product.id,
                product_template.name as name,
                product_category.name               AS product_category
            FROM product_product product
                LEFT JOIN product_template          ON product_template.id = product.product_tmpl_id
                LEFT JOIN product_category          ON product_category.id = product_template.categ_id
            )""")
