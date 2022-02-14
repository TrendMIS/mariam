from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    international_phone = fields.Char(related='partner_id.international_phone', readonly=True)
    extra_phone = fields.Char(related='partner_id.extra_phone', readonly=True)
