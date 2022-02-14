from odoo import models, fields


class Stage(models.Model):
    _inherit = "crm.stage"

    is_lost = fields.Boolean('Is Lost Stage?')
