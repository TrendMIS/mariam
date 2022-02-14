# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Lead(models.Model):
    _inherit = 'crm.lead'

    name = fields.Many2one('real.estate.project', string='Project', required=True, index=True)
