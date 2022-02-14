# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_real_estate_unit = fields.Boolean(string='Is A Real Estate Unit')
    developer_id = fields.Many2one('res.partner', string='Developer', domain=[('developer', '=', True)])
    unit_area = fields.Float(string='Area')
    unit_meter_price = fields.Float(string='Meter Price')
    unit_net_area = fields.Float(string='Net Area')
    list_price = fields.Float(string='Estimated Price', compute='get_unit_price', store=True,
                              digits=dp.get_precision('Product Price'),
                              help="Base price to compute the customer price. Sometimes called the catalog price.")
    full_unit_price = fields.Float(string='Full Unit Price')
    state = fields.Selection(string="Status", selection=[
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold')
    ], default='available')
    floor = fields.Char(string='Floor')
    terrace = fields.Text()
    roof_area = fields.Float()

    @api.depends('unit_area', 'unit_meter_price')
    def get_unit_price(self):
        for rec in self:
            if rec.is_garage or rec.is_club != False:
                for product in self:
                    product.list_price = product.list_price
            else:
                for product in self:
                    product.list_price = product.unit_area * product.unit_meter_price
