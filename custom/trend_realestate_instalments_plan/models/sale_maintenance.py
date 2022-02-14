# -*-	coding:	utf-8	-*-
from odoo import models, api, fields, _
from odoo.exceptions import UserError


class Installment(models.Model):
    _name = "sale.maintenance"
    _description = "Maintenance"
    _inherit = "mail.thread"

    sale_id_main = fields.Many2one(comodel_name="sale.order", required=True, ondelete='cascade')
    maintenance_date = fields.Date(copy=False)
    maintenance_amount = fields.Float()
    status = fields.Selection(string="Payment Status", selection=[('paid', 'Paid'),
                                                                  ('not_paid', 'Not Paid')],
                              copy=False, default='not_paid')
    name = fields.Char(string="Seq", required=True, copy=False, default='New')
    related_payment_ids = fields.One2many("account.payment", "maintenance_id",
                                          string="Related Payments", readonly=True)

    def create_maintenance_payments(self):
        related_payments_total = sum(self.related_payment_ids.mapped("amount"))
        remaining_payment_amount = round(self.maintenance_amount) - related_payments_total
        if remaining_payment_amount == 0:
            raise UserError("This maintenance already has payments with the total amount")
        self.env['account.payment'].create({
            'maintenance_id': self.id,
            'maintenance_sale_id': self.sale_id_main.id,
            'partner_id': self.sale_id_main.partner_id.id,
            'amount': remaining_payment_amount,
            'currency_id': self.sale_id_main.currency_id.id,
            'journal_id': self.sale_id_main._get_default_journal_id(),
            'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
            'payment_type': 'inbound',
            'partner_type': 'customer',
        })
