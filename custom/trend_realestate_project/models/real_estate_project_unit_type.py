# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class RealEstateProjectUnitType(models.Model):
    _name = 'real.estate.project.unit.type'
    _description = 'Real Estate Project Unit Type'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    real_estate_project_id = fields.Many2one('real.estate.project', string='Real Estate Project', ondelete='cascade')
