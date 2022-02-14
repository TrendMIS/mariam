from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    lost_reason_project_id = fields.Many2one('real.estate.project')
