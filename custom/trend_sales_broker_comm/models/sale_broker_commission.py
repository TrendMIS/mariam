# -*-	coding:	utf-8	-*-

import calendar
from odoo import models, api, fields, _
from datetime import datetime


class AccountMove(models.Model):
    _inherit = "account.move"

    sale_broker_commission_id = fields.Many2one("sale.broker.commission")


class BrokerCommission(models.Model):
    _name = "sale.broker.commission"
    _description = "Sales Broker Commission"
    _inherit = "mail.thread"
    _rec_name = 'display_name'

    from_date = fields.Date()
    to_date = fields.Date()
    broker_id = fields.Many2one("res.partner", string="Broker", domain=[('is_broker', '=', True)], required=True)
    program_id = fields.Many2one("broker.commission.program")
    sale_info_ids = fields.One2many("commission.sale.info", "commission_id")

    commission = fields.Float(copy=False)
    display_name = fields.Char('Display Name', compute='_compute_complete_name', store=True)

    @api.depends('broker_id', 'from_date', 'to_date')
    def _compute_complete_name(self):
        for record in self:
            record.display_name = '%s -  %s to %s' % (record.broker_id.name, record.from_date, record.to_date)

    def action_compute_commission(self):
        self.sale_info_ids.unlink()
        sale_order_domain = [('state', 'in', ['done', 'sale']),
                             ('date_order', '>=', self.from_date),
                             ('date_order', '<=', self.to_date)]
        field = "broker_id" if self.broker_id.company_type == 'company' else "broker_salesman_id"
        sale_order_domain.append((field, '=', self.broker_id.id))
        sales_orders = self.env['sale.order'].sudo().search(sale_order_domain)
        if not sales_orders:
            return
        self._create_sales_info_from(sales_orders)
        total_sales_amount = sum(sales_orders.mapped("amount_total"))
        broker_program_line = self.program_id.line_ids.filtered(
            lambda l: l.target_from <= total_sales_amount <= l.target_to
        )
        if broker_program_line:
            self.commission = (broker_program_line.commission_percentage * total_sales_amount) / 100

    def action_view_invoice(self):
        action = self.env.ref('account.action_move_in_invoice_type')
        result = action.read()[0]
        # override the context to get rid of the default filtering
        invoice_vals = {
            'type': 'in_invoice',
            'partner_id': self.broker_id.id,
            'sale_broker_commission_id': self.id,
            'invoice_line_ids': [(0, 0, {
                "quantity": 1,
                "price_unit": self.commission,
            })]
        }
        bill = self.env["account.move"].sudo().create(invoice_vals)

        res = self.env.ref('account.view_move_form', False)
        form_view = [(res and res.id or False, 'form')]
        if 'views' in result:
            result['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
        else:
            result['views'] = form_view

        result['res_id'] = bill.id

        return result

    def _create_sales_info_from(self, sales_orders):
        for order in sales_orders:
            self.env['commission.sale.info'].create({
                "commission_id": self.id,
                "sale_id": order.id,
                "unit_id": order.order_line[0].product_id.id
            })


class CommissionSaleInfo(models.Model):
    _name = "commission.sale.info"

    commission_id = fields.Many2one("sale.broker.commission")
    sale_id = fields.Many2one("sale.order")
    unit_id = fields.Many2one("product.product")
    date_order = fields.Datetime(related="sale_id.date_order")
    full_unit_price = fields.Float(related="sale_id.full_unit_price")
    broker_id = fields.Many2one("res.partner", related="sale_id.broker_id")
    customer_id = fields.Many2one("res.partner", related="sale_id.partner_id")
    broker_salesman_id = fields.Many2one("res.partner", related="sale_id.broker_salesman_id")
