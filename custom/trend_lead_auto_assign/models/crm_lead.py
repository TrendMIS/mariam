# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    campaign_id = fields.Many2one()

    @api.model
    def create(self, vals):
        if vals.get("campaign_id") and not self.env.context.get("copy"):
            self._assign_team(vals)
        return super().create(vals)

    def write(self, vals):
        if vals.get("campaign_id"):
            self._assign_team(vals)
        return super().write(vals)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        ctx = dict(self.env.context)
        ctx['copy'] = True
        default = dict(default or {})
        default['team_id'] = None
        default['user_id'] = None
        return super(CrmLead, self.with_context(ctx)).copy(default=default)

    def _assign_team(self, vals):
        assigned_team = self._get_assigned_team(vals['campaign_id'])
        if not assigned_team:
            return
        vals['team_id'] = assigned_team.id
        vals['user_id'] = assigned_team.user_id and assigned_team.user_id.id

    def _get_assigned_team(self, campaign_id):
        assigned_team = None
        minimum_leads = 10 ** 10  # Assume the minimum as a very big number
        for team in self.env['crm.team'].search([]):
            team_leads_count = self.search_count([('team_id', '=', team.id), ('campaign_id', '=', campaign_id)])
            if team_leads_count < minimum_leads:
                minimum_leads = team_leads_count
                assigned_team = team
        return assigned_team
