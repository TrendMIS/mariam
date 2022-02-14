# -*-	coding:	utf-8	-*-
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    apply_mobile_validation_on_partner = fields.Boolean(string='Apply Mobile Validation On Partner')

    def set_values(self):
        set_param = self.env['ir.config_parameter'].set_param
        set_param('apply_mobile_validation_on_partner', (self.apply_mobile_validation_on_partner))
        super(ResConfigSettings, self).set_values()

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            apply_mobile_validation_on_partner=bool(get_param('apply_mobile_validation_on_partner')),
        )
        return res
