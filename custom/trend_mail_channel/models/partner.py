from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_related_user = fields.Boolean(string="Related User", compute='_compute_is_related_user', store=True)

    def _compute_is_related_user(self):
        for rec in self:
            record = self.env['res.users'].search_count([('partner_id', '=', rec.id)])
            if record:
                rec.is_related_user = True
            else:
                rec.is_related_user = False
