from odoo import fields, models, api


class CrmLeadType(models.Model):
    _name = "crm.lead.type"
    _description = "Lead types"

    name = fields.Char()


class CrmLead(models.Model):
    _inherit = "crm.lead"
    _description = "Leads"

    lead_type_id = fields.Many2one("crm.lead.type")
