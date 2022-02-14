# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_garage = fields.Boolean(string='Is A Garage')
    garage_related_block = fields.Char()
    is_club = fields.Boolean(string="Is A Club Membership")
