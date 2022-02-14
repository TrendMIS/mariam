# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    user_team_id = fields.Many2one('crm.team', related='user_id.sale_team_id', store=True)
