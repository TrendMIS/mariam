# -*-	coding:	utf-8	-*-
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    commission_product_id = fields.Many2one('product.product', string='Commission Product')

    def set_values(self):
        set_param = self.env['ir.config_parameter'].set_param
        set_param('commission_product_id', (self.commission_product_id.id))
        super(ResConfigSettings, self).set_values()

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            commission_product_id=int(get_param('commission_product_id')),
        )
        return res
