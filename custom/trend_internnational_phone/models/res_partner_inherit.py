# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    international_phone = fields.Char()
    extra_phone = fields.Char()

    @api.constrains('mobile', 'phone', 'international_phone', 'extra_phone')
    def check_mobile_value(self):
        should_verify = self.env['ir.config_parameter'].sudo().get_param('apply_mobile_validation_on_partner')
        if not bool(should_verify):
            return
        for partner in self:
            numbers = []
            if partner.mobile:
                numbers.append(partner.mobile[-10:])
            if partner.phone:
                numbers.append(partner.phone[-10:])
            if partner.international_phone:
                numbers.append(partner.international_phone[-10:])
            if partner.extra_phone:
                numbers.append(partner.extra_phone[-10:])
            if not numbers:
                return True
            query = """
            SELECT id FROM res_partner 
            WHERE id != %(partner_id)s
            AND (
                RIGHT(mobile, 10) in %(numbers)s OR 
                RIGHT(phone, 10) in %(numbers)s OR
                RIGHT(international_phone, 10) in %(numbers)s OR
                RIGHT(extra_phone, 10) in %(numbers)s
            );
            """
            self._cr.execute(query, {"partner_id": partner.id, "numbers": tuple(numbers)})
            partner_objects = self._cr.fetchall()
            if partner_objects:
                raise ValidationError(_('One of the phone numbers already exists.'))
