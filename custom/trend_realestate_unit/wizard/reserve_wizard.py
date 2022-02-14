# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ReserveWizard(models.TransientModel):
    _name = 'realestate.reserve.wizard'
    _description = 'Reserve a unit'

    reservation_date = fields.Date(default=datetime.today())
    reservation_expiry_date = fields.Date(compute="compute_reservation_expiry_date")
    reservation_deposit_amount = fields.Float()

    @api.onchange('reservation_date')
    def compute_reservation_expiry_date(self):
        self.reservation_expiry_date = fields.Datetime.from_string(self.reservation_date) + relativedelta(days=7)

    def reserve(self):
        sale_order = self.env['sale.order'].browse(self.env.context['active_id'])
        sale_order.write({
            "reservation_date": self.reservation_date,
            "reservation_expiry_date": self.reservation_expiry_date,
            "reservation_deposit_amount": self.reservation_deposit_amount,
            "state": "reserved"
        })
        units = sale_order.order_line.filtered(lambda l: l.product_id.is_real_estate_unit).mapped('product_id')
        units.write({"state": "reserved"})
