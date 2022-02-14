# -*- coding: utf-8 -*-

from odoo import fields, models


class CrmLeadLost(models.TransientModel):
    _inherit = 'crm.lead.lost'
    _description = 'Get Lost Reason'

    lost_reason_project_id = fields.Many2one('real.estate.project')

    def action_lost_reason_apply(self):
        super().action_lost_reason_apply()
        leads = self.env['crm.lead'].browse(self.env.context.get('active_ids'))
        return leads.write({"lost_reason_project_id": self.lost_reason_project_id.id})
