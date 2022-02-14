# -*-	coding:	utf-8	-*-
from odoo import models, api, fields, _
from odoo.exceptions import UserError


class SaleInstallment(models.Model):
    _name = "sale.additional.installment"
    _description = "Additional Installment"
    _inherit = "mail.thread"
    _order = 'name'

    sale_id = fields.Many2one(comodel_name="sale.order", required=True, ondelete='cascade')
    partner_id = fields.Many2one(related="sale_id.partner_id")
    installment_date = fields.Date(copy=False, string="Date", required=True, )
    installment_amount = fields.Float(string="Amount", required=True, )

    name = fields.Integer(string="Seq", required=True, copy=False, default='0')
