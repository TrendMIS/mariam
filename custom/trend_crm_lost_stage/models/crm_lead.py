from odoo import models


class CrmLeadInherit(models.Model):
    _inherit = 'crm.lead'

    def action_set_lost(self, **additional_values):
        super().action_set_lost(**additional_values)
        lost_stage = self.env["crm.stage"].search([('is_lost', '=', True)])
        for lead in self:
            for stage in lost_stage:
                lead.write({'stage_id': stage.id, 'probability': 0})
        return True
