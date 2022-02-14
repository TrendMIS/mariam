from odoo import fields, models, api


class CrLead(models.Model):
    _inherit = "crm.lead"

    status_ids = fields.Many2many(comodel_name="status.type", string="Status Types", compute='compute_status_ids',
                                  store=True)

    @api.depends('stage_id')
    def compute_status_ids(self):
        for rec in self:
            rec.status_ids = rec.stage_id.status_ids
