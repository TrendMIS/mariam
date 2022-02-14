# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Lead(models.Model):
    _inherit = 'crm.lead'

    broker_salesman_id = fields.Many2one("res.partner", string="Broker Salesman",
                                         domain="[('is_broker', '=', True), ('parent_id', '=', broker_id)]")

    def action_new_quotation(self):
        action = super(Lead, self).action_new_quotation()
        action['context'].update({
            'default_broker_salesman_id': self.broker_salesman_id.id,
            'default_broker_id': self.broker_id.id,

        })
        return action
