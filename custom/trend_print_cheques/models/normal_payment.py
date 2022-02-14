from odoo import api, fields, models


class Payment(models.Model):
    _inherit = 'normal.payments'

    cheque_format_id = fields.Many2one(comodel_name="cheque.configuration", string="Cheque Format", required=False, )

    recipient_name = fields.Char(string="Recipient Name", default=lambda self: self.env.company.name)
