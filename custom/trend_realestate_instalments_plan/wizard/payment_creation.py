from odoo import models, fields, api


class PaymentCreationWizard(models.TransientModel):
    _name = "payment.creation.wizard"

    installment_ids = fields.Many2many('sale.installment')

    @api.onchange('installment_ids')
    def set_domain(self):
        active_ids = self.env.context.get('active_ids')
        sale_installments = self.env['sale.installment'].search([('sale_id', 'in', active_ids)])
        actual_installment = []
        for installment in sale_installments:
            related_payments_total = sum(installment.related_payment_ids.mapped("amount"))
            if installment.installment_amount > related_payments_total:
                actual_installment.append(installment.id)
        return {'domain': {'installment_ids': [('id', 'in', actual_installment)]}}

    def confirm_payment(self):
        print("confirm")
        for installment in self.installment_ids:
            installment.create_installments_payments()
