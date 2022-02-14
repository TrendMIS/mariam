# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    is_real_estate = fields.Boolean(string='Real Estate')
