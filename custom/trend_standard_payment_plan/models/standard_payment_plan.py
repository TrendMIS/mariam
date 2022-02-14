from odoo import models, fields, api


class StandardPaymentPlan(models.Model):
    _name = 'standard.payment.plan'
    name = fields.Char()
    contract_signing_per = fields.Float(string="Contract Signing Percentage")
    delivery_percentage = fields.Float(string="Delivery Percentage")
    no_of_installments = fields.Integer()
    installments_frequency = fields.Selection(
        [('monthly', 'Monthly'),
         ('quarter', 'Quarter'),
         ('4_months', '4 Months'),
         ('semi_annual', 'Semi Annual'),
         ('annual', 'Annual'),
         ],
        copy=False, default='monthly')
    first_installment_after = fields.Integer(string="First Installments After")
