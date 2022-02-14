# -*-	coding:	utf-8	-*-
from odoo import models, api, fields, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math
import datetime


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    @api.onchange('reservation_date')
    def _get_first_instalments_date(self):
        if self.reservation_date:
            self.first_installment_date = self.reservation_date + relativedelta(months=3)

    installment_ids = fields.One2many(comodel_name="sale.installment", inverse_name="sale_id")
    maintenance_ids = fields.One2many(comodel_name="sale.maintenance", inverse_name="sale_id_main")
    deposit_amount = fields.Float()
    residual_amount = fields.Float('Residual Contract Signing Amount', compute='get_residual_amount',
                                   store=True)
    contract_signing_amount = fields.Float()
    delivery_amount = fields.Float()
    delivery_amount_per = fields.Float("Delivery Percentage")
    contract_amount_per = fields.Float("Contract Signing Percentage")
    maintenance_per = fields.Float("Maintenance Percentage")
    maintenance_amount = fields.Float("Maintenance Amount", compute='get_maintenance_amount',
                                      store=True)
    full_unit_price = fields.Float(string='Full Unit Price', compute='get_full_unit_price',
                                   store=True)
    first_installment_date = fields.Date(copy=False, default=_get_first_instalments_date)
    no_of_installments = fields.Integer()
    maintenance_no = fields.Integer()
    payment_type = fields.Selection(string="Payment Type", selection=[('monthly', 'Monthly'),
                                                                      ('quarter', 'Quarter'),
                                                                      ('4_months', '4 Months'),
                                                                      ('semi_annual', 'Semi Annual'),
                                                                      ('annual', 'Annual'),
                                                                      ],
                                    copy=False, default='monthly')

    installment_amount = fields.Float(compute='get_installment_amount',
                                      store=True)

    deposit_amount_date = fields.Date(string='Deposit Date')
    contract_signing_amount_date = fields.Date(string='Contract Signing Date')
    delivery_amount_date = fields.Date(string='Delivery Date')
    standard_payment_plan_id = fields.Many2one('standard.payment.plan')
    project_id = fields.Many2one("real.estate.project", compute="get_project", store=True)
    maintenance_after_discount = fields.Boolean()
    contract_signing_amount_after_discount = fields.Boolean()
    installment_corrected_value = fields.Float()
    is_additional = fields.Boolean(string="Additional Options", )
    additional_installments = fields.Selection(string="Additional Installments", selection=[
        ('regular', 'Regular'),
        ('irregular', 'Irregular Installments'),
    ], required=False, )

    additional_installment_date = fields.Date(string="First Installment Date")
    additional_installment_number = fields.Integer(string="Installment Number")
    additional_installment_amount = fields.Float(string="Installment Amount")

    additional_payment_type = fields.Selection(string="Additional Payment Type", selection=[('monthly', 'Monthly'),
                                                                                            ('quarter', 'Quarter'),
                                                                                            ('4_months', '4 Months'),
                                                                                            ('semi_annual',
                                                                                             'Semi Annual'),
                                                                                            ('annual', 'Annual'),
                                                                                            ],
                                               copy=False, default='monthly')

    additional_installment_ids = fields.One2many(comodel_name="sale.additional.installment", inverse_name="sale_id")

    @api.onchange('additional_installment_ids')
    def _onchange_additional_installment(self):
        if self.additional_installment_ids:
            self.additional_installment_amount = sum(self.additional_installment_ids.mapped('installment_amount'))

    @api.constrains('additional_installment_amount')
    def check_additional_installment_amount(self):
        for order in self:
            if order.full_unit_price and order.additional_installment_amount:
                if order.additional_installment_amount > order.full_unit_price:
                    raise ValidationError(_('Additional installments amount must be Less Than full unit price.'))

    @api.depends('order_line.product_id')
    def get_project(self):
        for order in self:
            if order.order_line:
                order.project_id = order.order_line[0].product_id.real_estate_project_id
            else:
                order.project_id = 0.0

    @api.onchange('standard_payment_plan_id')
    def _onchange_standard_payment_plan_id(self):
        self.payment_type = self.standard_payment_plan_id.installments_frequency
        self.contract_amount_per = self.standard_payment_plan_id.contract_signing_per
        self.delivery_amount_per = self.standard_payment_plan_id.delivery_percentage
        self.no_of_installments = self.standard_payment_plan_id.no_of_installments
        today = datetime.date.today()
        self.first_installment_date = today + relativedelta(
            months=self.standard_payment_plan_id.first_installment_after)

    @api.constrains('full_unit_price', 'installment_ids')
    def check_total_installment_amount(self):
        for order in self:
            if order.full_unit_price and order.installment_ids:
                if order.full_unit_price != sum(
                        installment.installment_amount for installment in order.installment_ids):
                    raise ValidationError(_('Total installments amount must be equal full unit price.'))

    @api.onchange('contract_amount_per', 'full_unit_price', 'contract_signing_amount_after_discount')
    @api.depends('contract_amount_per', 'full_unit_price', 'contract_signing_amount_after_discount')
    def get_contract_amount(self):
        if not self.contract_signing_amount_after_discount:
            for order in self:
                if order.order_line:
                    order.contract_signing_amount = order.order_line[0].price_unit * (order.contract_amount_per / 100)
        else:
            for order in self:
                order.contract_signing_amount = order.full_unit_price * (order.contract_amount_per / 100)

    @api.onchange('contract_signing_amount', 'full_unit_price')
    @api.depends('contract_signing_amount', 'full_unit_price')
    def get_contract_per(self):
        for order in self:
            if order.full_unit_price > 0:
                order.contract_amount_per = (order.contract_signing_amount / order.full_unit_price) * 100

    @api.onchange('contract_signing_amount', 'full_unit_price', 'deposit_amount')
    @api.depends('contract_signing_amount', 'full_unit_price', 'deposit_amount')
    def get_residual_amount(self):
        for order in self:
            order.residual_amount = order.contract_signing_amount - order.deposit_amount

    @api.onchange('delivery_amount_per', 'full_unit_price')
    @api.depends('delivery_amount_per', 'full_unit_price')
    def get_delivery_amount(self):
        for order in self:
            order.delivery_amount = order.full_unit_price * (order.delivery_amount_per / 100)

    @api.onchange('delivery_amount', 'full_unit_price')
    @api.depends('delivery_amount', 'full_unit_price')
    def get_delivery_per(self):
        for order in self:
            if order.full_unit_price > 0:
                order.delivery_amount_per = (order.delivery_amount / order.full_unit_price) * 100

    @api.depends('order_line', 'order_line.product_id', 'order_line.price_subtotal')
    def get_full_unit_price(self):
        for order in self:
            if order.order_line:
                order.full_unit_price = order.order_line[0].price_subtotal
            else:
                order.full_unit_price = 0.0

    @api.depends('maintenance_per', 'full_unit_price', 'maintenance_after_discount')
    def get_maintenance_amount(self):
        for order in self:
            if not order.maintenance_after_discount:
                if order.order_line:
                    order.maintenance_amount = order.order_line[0].price_unit * (order.maintenance_per / 100)
            else:
                order.maintenance_amount = order.full_unit_price * (order.maintenance_per / 100)

    @api.depends('deposit_amount', 'contract_signing_amount', 'delivery_amount', 'full_unit_price')
    def get_installment_amount(self):
        for order in self:
            order.installment_amount = order.full_unit_price - (
                    order.contract_signing_amount + order.delivery_amount)

    def _check_data_before_submit(self):
        if not self.first_installment_date:
            raise ValidationError(_("You must provide installment first date before create installments"))

        if not self.deposit_amount_date and self.deposit_amount:
            raise ValidationError(_("You must provide deposit date before create installments"))

        if not self.contract_signing_amount_date and self.contract_signing_amount:
            raise ValidationError(_("You must provide contract signing date before create installments"))

        if not self.delivery_amount_date and self.delivery_amount:
            raise ValidationError(_("You must provide delivery date before create installments"))

        if not self.no_of_installments:
            raise ValidationError(_("You must provide number of installments before create installments"))

        if not self.order_line:
            raise ValidationError(_("You must provide Unit before create installments"))

    def action_create_main(self):
        if self.maintenance_ids:
            self.sudo().maintenance_ids.unlink()
        if not self.maintenance_no:
            raise ValidationError(_("You must provide maintenance number before create maintenance"))

        if not self.maintenance_after_discount:
            all_amount = self.order_line[0].price_unit * (self.maintenance_per / 100)
        else:
            all_amount = self.full_unit_price * (self.maintenance_per / 100)
        m_amount = all_amount / self.maintenance_no
        for counter in range(0, self.maintenance_no):
            main_vals = {
                "name": counter + 1,
                "sale_id_main": self.id,
                "maintenance_amount": m_amount,

            }
            main_id = self.env['sale.maintenance'].sudo().create(main_vals)
            all_amount = all_amount - m_amount
            if all_amount < m_amount:
                m_amount = all_amount

    def action_create_installments(self):
        self._check_data_before_submit()
        if self.installment_ids:
            self.sudo().installment_ids.unlink()

        installment_date = fields.Date.from_string(self.first_installment_date)
        installment_amount = self.installment_amount / self.no_of_installments
        if self.payment_type == 'monthly':
            months = 1
        elif self.payment_type == 'quarter':
            months = 3
        elif self.payment_type == '4_months':
            months = 4
        elif self.payment_type == 'semi_annual':
            months = 6
        else:
            months = 12
        counter = 0
        installment_vals = []
        for counter in range(1, self.no_of_installments + 1):
            if self.installment_corrected_value == 0:
                digit_remaining_amount, int_remaining_amount = math.modf(installment_amount)
                remaining_amount = digit_remaining_amount * (self.no_of_installments - 1)
                if counter != (self.no_of_installments):
                    installment_vals += [{
                        "sale_id": self.id,
                        "installment_date": installment_date,
                        "installment_amount": int_remaining_amount,
                        "installment_type": 'regular',

                    }]
                    remaining_amount += digit_remaining_amount
                    installment_date = installment_date + relativedelta(months=months)
                elif counter == (self.no_of_installments):
                    installment_vals += [{
                        "sale_id": self.id,
                        "installment_date": installment_date,
                        "installment_amount": installment_amount + remaining_amount,
                        "installment_type": 'regular',

                    }]
                    installment_date = installment_date + relativedelta(months=months)
            else:
                if counter != (self.no_of_installments):
                    installment_vals += [{
                        "sale_id": self.id,
                        "installment_date": installment_date,
                        "installment_amount": self.installment_corrected_value,
                        "installment_type": 'regular',

                    }]
                    installment_date = installment_date + relativedelta(months=months)
                elif counter == self.no_of_installments:
                    installment_vals += [{
                        "sale_id": self.id,
                        "installment_date": installment_date,
                        "installment_amount": (
                                self.installment_amount - (
                                self.installment_corrected_value * (self.no_of_installments - 1))),
                        "installment_type": 'regular',
                    }]
                    installment_date = installment_date + relativedelta(months=months)
        if self.contract_signing_amount:
            installment_vals += [{
                "sale_id": self.id,
                "installment_date": fields.Date.from_string(self.contract_signing_amount_date),
                "installment_amount": self.residual_amount if self.residual_amount else (
                            self.contract_signing_amount - self.deposit_amount),
                "installment_type": 'contract_signing',

            }]

        if self.delivery_amount:
            installment_vals += [{
                "sale_id": self.id,
                "installment_date": fields.Date.from_string(self.delivery_amount_date),
                "installment_amount": self.delivery_amount,
                "installment_type": 'delivery',

            }]
        if self.deposit_amount:
            installment_vals += [{
                "sale_id": self.id,
                "installment_date": fields.Date.from_string(self.deposit_amount_date),
                "installment_amount": self.deposit_amount,
                "installment_type": 'deposit',

            }]
        new_installment_vals = sorted(installment_vals, key=lambda k: k['installment_date'])
        for counter in range(0, len(new_installment_vals)):
            new_installment_vals[counter].update({"name": counter + 1})

        for item in new_installment_vals:
            created_installments = self.env['sale.installment'].sudo().create(item)

    def action_confirm(self):
        super().action_confirm()
        result = self.call_wizard()
        return result

    def call_wizard(self):
        return {
            'name': 'Sales Order Confirmation',
            'res_model': 'payment.creation.wizard',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }

    def _get_default_journal_id(self):
        journal = self.env['account.move']._search_default_journal(('bank', 'cach'))
        if not journal:
            raise UserError(_(f'Please define an accounting sales journal for the company {self.company_id.name}'))
        return journal.id


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if self.product_id and self.product_id.full_unit_price:
            self.price_unit = self.product_id.full_unit_price
        else:
            return super(SaleOrderLine, self).product_uom_change()
