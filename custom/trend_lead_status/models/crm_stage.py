from odoo import fields, models


class CrmStage(models.Model):
    _inherit = "crm.stage"

    status_ids = fields.Many2many(comodel_name="status.type", string="Status", )
