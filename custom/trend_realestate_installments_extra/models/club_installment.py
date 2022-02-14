# -*-	coding:	utf-8	-*-
from odoo import models, fields


class ClubInstallment(models.Model):
    _name = "club.installment"
    _description = "Club Installment"
    _inherit = "mail.thread"

    name = fields.Integer(string="Seq", required=True, copy=False, default='0')
    sale_id = fields.Many2one(comodel_name="sale.order", required=True, ondelete='cascade')
    installment_date = fields.Date(copy=False, string="Date")
    installment_amount = fields.Float(string="Amount")
