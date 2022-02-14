# -*-	coding:	utf-8	-*-
from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import math


class SaleOrder(models.Model):
    _inherit = "sale.order"

    garage_installment_ids = fields.One2many(comodel_name="garage.installment", inverse_name="sale_id")
    garage_installments_count = fields.Integer("Garage Installments")
    club_installment_ids = fields.One2many(comodel_name="club.installment", inverse_name="sale_id")
    club_installments_count = fields.Integer("Club Installments")
    has_club = fields.Boolean(compute="_has_special_item")
    has_garage = fields.Boolean(compute="_has_special_item")

    def _has_special_item(self):
        for order in self:
            order.has_club = False
            order.has_garage = False
            for line in order.order_line:
                if line.product_id.is_club:
                    order.has_club = True
                if line.product_id.is_garage:
                    order.has_garage = True

    def action_create_club_installments(self):
        self._validate_club_installments()
        total_amount = self._get_club_total_amount()
        installment_amount = total_amount / self.club_installments_count
        for counter in range(0, self.club_installments_count):
            self.env['club.installment'].sudo().create({
                "name": counter + 1,
                "sale_id": self.id,
                "installment_amount": installment_amount,
            })
            total_amount -= installment_amount
            if total_amount < installment_amount:
                installment_amount = total_amount

    def _validate_club_installments(self):
        if self.club_installment_ids:
            self.sudo().club_installments_ids.unlink()
        if not self.club_installments_count:
            raise ValidationError(_("You must provide club installments count before creating installments"))

    def _get_club_total_amount(self):
        for line in self.order_line:
            if line.product_id.is_club:
                return line.price_unit
        return 0

    def action_create_garage_installments(self):
        self._validate_garage_installments()
        total_amount = self._get_garage_total_amount()
        installment_amount = total_amount / self.garage_installments_count
        for counter in range(0, self.garage_installments_count):
            self.env['garage.installment'].sudo().create({
                "name": counter + 1,
                "sale_id": self.id,
                "installment_amount": installment_amount,
            })
            total_amount -= installment_amount
            if total_amount < installment_amount:
                installment_amount = total_amount

    def _validate_garage_installments(self):
        if self.garage_installment_ids:
            self.sudo().garage_installments_ids.unlink()
        if not self.garage_installments_count:
            raise ValidationError(_("You must provide garage installments count before creating installments"))

    def _get_garage_total_amount(self):
        for line in self.order_line:
            if line.product_id.is_garage:
                return line.price_unit
        return 0
