# -*-	coding:	utf-8	-*-
from odoo import models, api, fields, _
from odoo.exceptions import UserError


class SaleInstallment(models.Model):
    _name = "sale.installment"
    _description = "Installment"
    _inherit = "mail.thread"

    @api.depends("installment_amount")
    def calc_cumulative(self):
        for rec in self:
            previous_installments = rec.sale_id.installment_ids
            if rec.id:
                previous_installments = rec.sale_id.installment_ids.filtered(lambda r: r.id <= rec.id)
            posted_payments = rec.related_payment_ids.filtered(lambda r: r.state in ['posted', 'reconciled'])
            rec.actual_paid = sum(posted_payments.mapped('amount'))
            rec.status = rec.get_payment_status()
            rec.cumulative_amount = sum(previous_installments.mapped("installment_amount"))
            rec.cumulative_payments = sum(previous_installments.mapped("actual_paid"))
            rec.overdue_amounts = rec.cumulative_amount - rec.cumulative_payments
            percentage = round((rec.cumulative_amount / rec.sale_id.full_unit_price) * 100, 2)
            rec.cumulative_percentage = f"{percentage}%"

    sale_id = fields.Many2one(comodel_name="sale.order", required=True, ondelete='cascade')
    partner_id = fields.Many2one(related="sale_id.partner_id")
    cumulative_amount = fields.Float(compute="calc_cumulative")
    cumulative_percentage = fields.Char(compute="calc_cumulative", string='Cumulative Percentage')
    installment_date = fields.Date(copy=False, string="Date")
    installment_amount = fields.Float(string="Amount")
    discount = fields.Float(string='Discount')
    status = fields.Selection(string="Payment Status",
                              selection=[('paid', 'Paid'), ('partial', "Partially paid"), ('not_paid', 'Not Paid')],
                              compute="calc_cumulative")
    name = fields.Integer(string="Seq", required=True, copy=False, default='0')

    installment_type = fields.Selection(string="Type", selection=[
        ('regular', 'Regular Installment'),
        ('delivery', 'Delivery Amount'),
        ('deposit', 'Deposit Amount'),
        ('contract_signing', 'Contract Signing Amount'),
        ('additional', 'Additional Installment'),
    ])

    related_payment_ids = fields.One2many("account.payment", "installment_id",
                                          string="Related Payments", readonly=True)
    actual_paid = fields.Float(compute="calc_cumulative")
    cumulative_payments = fields.Float(compute="calc_cumulative")
    overdue_amounts = fields.Float(compute="calc_cumulative")

    def create_installments_payments(self, skip=False):
        related_payments_total = sum(self.related_payment_ids.mapped("amount"))
        remaining_payment_amount = self.installment_amount - related_payments_total
        if remaining_payment_amount == 0:
            skip = True
            if skip:
                return
            # raise UserError("This installment already has payments with the total amount")
        self.env['account.payment'].create({
            'installment_id': self.id,
            'sale_id': self.sale_id.id,
            'partner_id': self.partner_id.id,
            'amount': remaining_payment_amount,
            'currency_id': self.sale_id.currency_id.id,
            'journal_id': self.sale_id._get_default_journal_id(),
            'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
            'payment_type': 'inbound',
            'partner_type': 'customer',
        })

    def get_payment_status(self):
        if self.actual_paid == self.installment_amount:
            return 'paid'
        if self.actual_paid == 0:
            return "not_paid"
        return "partial"
