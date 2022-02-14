from odoo import api, fields, models


class Users(models.Model):
    _inherit = 'res.users'

    is_salesperson = fields.Boolean()
