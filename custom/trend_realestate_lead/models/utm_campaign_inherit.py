# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class UTMCampaign(models.Model):
    _inherit = 'utm.campaign'

    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')
    campaign_budget = fields.Float(string='Campaign Budget')
    leads_count = fields.Integer(string='Leads', compute='get_campaign_leads')

    def get_campaign_leads(self):
        for campaign in self:
            campaign.leads_count = self.env['crm.lead'].sudo().search_count([('campaign_id', '=', campaign.id)])

    def open_campaign_leads(self):
        for campaign in self:
            campaign_leads_objects = self.env['crm.lead'].sudo().search([('campaign_id', '=', campaign.id)])
            form_view_id = self.env.ref('crm.crm_lead_view_form')
            tree_view_id = self.env.ref('crm.crm_case_tree_view_oppor')
            return {
                'name': _('Leads'),
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'res_model': 'crm.lead',
                'views': [(tree_view_id.id, 'tree'), (form_view_id.id, 'form')],
                'view_id': tree_view_id.id,
                'target': 'current',
                'domain': [('id', 'in', campaign_leads_objects.ids)],
            }

    @api.constrains('date_from', 'date_to')
    def check_dates_values(self):
        for campaign in self:
            if campaign.date_from and campaign.date_to and campaign.date_from > campaign.date_to:
                raise ValidationError(_('Date from must be less than date to!'))
