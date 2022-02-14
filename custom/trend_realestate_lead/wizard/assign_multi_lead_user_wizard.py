# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AssignMultiLeadUserWizard(models.TransientModel):
    _name = 'assign.multi.lead.user.wizard'
    _description = 'Assign Multi Lead User Wizard'

    user_id = fields.Many2one("res.users", string="Salesperson", required=True)

    def action_confirm_selected_user(self):
        for lead in self.env['crm.lead'].browse(self.env.context['multi_lead_ids']):
            lead.user_id = self.user_id.id
