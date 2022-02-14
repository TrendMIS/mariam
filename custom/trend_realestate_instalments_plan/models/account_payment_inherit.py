from odoo import models, fields
from odoo.exceptions import ValidationError


class AccountPaymentInherit(models.Model):
    _inherit = "account.payment"

    installment_id = fields.Many2one("sale.installment", readonly=False, ondelete='cascade')
    maintenance_id = fields.Many2one("sale.maintenance", readonly=False, ondelete='cascade')
    sale_id = fields.Many2one(string='Sale', related="installment_id.sale_id", readonly=False, store=True)
    maintenance_sale_id = fields.Many2one(string="Sale", related="maintenance_id.sale_id_main", readonly=False, store=True)

    def delete_installment_payment(self):
        if self.state == 'draft':
            if self.installment_id or self.maintenance_id:
                self.unlink()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
