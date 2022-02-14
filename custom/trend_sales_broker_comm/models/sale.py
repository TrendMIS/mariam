# -*-	coding:	utf-8	-*-

from odoo import models, api, fields, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    broker_id = fields.Many2one("res.partner", string="Broker",
                                domain="[('is_broker', '=', True), ('is_company', '=', True)]")
    broker_salesman_id = fields.Many2one("res.partner", string="Broker Salesman",
                                         domain="[('is_broker', '=', True), ('parent_id', '=', broker_id)]")
