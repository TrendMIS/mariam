# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    first_assignee_id = fields.Many2one('res.users', readonly=True)

    def write(self, vals):
        super().write(vals)
        for lead in self:
            if lead.first_assignee_id or not lead.user_id:
                return
            if (not lead.team_id and lead.user_id) or (lead.team_id and lead.user_id != lead.team_id.user_id):
                lead.first_assignee_id = lead.user_id
