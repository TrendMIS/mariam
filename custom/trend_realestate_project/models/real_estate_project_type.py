# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RealEstateProjectType(models.Model):
    _name = 'real.estate.project.type'
    _description = 'Real Estate Project Type'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
