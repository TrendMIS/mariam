# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    real_estate_project_id = fields.Many2one('real.estate.project', string='Real Estate Project', )
