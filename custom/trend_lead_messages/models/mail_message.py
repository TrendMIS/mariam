from odoo import fields, models, api

from html2text import HTML2Text


class CrmLead(models.Model):
    _inherit = "mail.message"

    clean_body = fields.Text(string="Clean Contents", compute='_compute_clean_body')

    @api.depends('body')
    def _compute_clean_body(self):
        html = HTML2Text()
        for rec in self:
            rec.clean_body = html.handle(rec.body)
