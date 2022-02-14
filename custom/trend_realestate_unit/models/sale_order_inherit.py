# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    reservation_date = fields.Date(string="Reservation Date")
    reservation_expiry_date = fields.Date(string="Reservation Expiry", readonly=True)
    reservation_deposit_amount = fields.Float(string="Reservation Deposit")
    state = fields.Selection(selection_add=[
        ('reserved', 'Reserved'),
        ('contract', 'Contract'),
        ('sale', 'Contract Signed and Received')
    ])

    def set_contract(self):
        self.write({"state": "contract"})

    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        for order in self:
            is_real_estate_units = order.order_line.filtered(lambda l: l.product_id.is_real_estate_unit).mapped(
                'product_id')
            if is_real_estate_units:
                is_real_estate_units.write({'state': 'sold'})

        return result

    def action_draft(self):
        super().action_draft()
        for record in self:
            record.state = 'draft'
            units = record.order_line.filtered(lambda l: l.product_id.is_real_estate_unit).mapped('product_id')
            units.write({"state": "available"})

    def unreserve_expired(self):
        expired_orders = self.search(
            [("reservation_expiry_date", "<", fields.datetime.today()), ('state', '=', 'reserved')])
        expired_orders.action_draft()
