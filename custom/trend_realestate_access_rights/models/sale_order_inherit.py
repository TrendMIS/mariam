# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('user_id')
    def set_user_id_team(self):
        for order in self:
            team_id = self.env['crm.team']._get_default_team_id(user_id=order.user_id.id)
            order.team_id = team_id
