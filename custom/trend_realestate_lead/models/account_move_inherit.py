# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    crm_lead_id = fields.Many2one('crm.lead', string='Lead')
    lead_unit_owner = fields.Char(string='Unit Owner', related='crm_lead_id.contract_name')
    lead_unit_number = fields.Char(string='Unit Number', related='crm_lead_id.unit_number')
    formal_company_name = fields.Char(string='Formal Company Name', related='partner_id.formal_company_name')
