from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    nationality = fields.Char()
