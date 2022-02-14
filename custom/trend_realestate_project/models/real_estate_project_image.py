# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class RealEstateProjectImage(models.Model):
    _name = 'real.estate.project.image'
    _description = 'Real Estate Project Image'

    name = fields.Char('Name')
    image = fields.Binary('Image', attachment=True)
    real_estate_project_id = fields.Many2one('real.estate.project', string='Real Estate Project',ondelete='cascade')
