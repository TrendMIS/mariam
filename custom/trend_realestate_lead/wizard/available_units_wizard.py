# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AvailableUnits(models.TransientModel):
    _name = 'available.units.wizard'

    product_ids = fields.Many2many('product.product',
                                   domain=[('is_real_estate_unit', '=', True),
                                           ('state', '=', 'available')],
                                   readonly=False)

    def confirm_unit(self):
        lead = self.env['crm.lead'].browse(self.env.context.get('active_ids'))
        lead.product_ids += self.product_ids
