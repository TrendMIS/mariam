# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RealEstateProject(models.Model):
    _name = 'real.estate.project'
    _description = 'Real Estate Project'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(default=True, )
    developer_id = fields.Many2one('res.partner', string='Developer', domain=[('developer', '=', True)])
    project_facility_ids = fields.Many2many('project.facility', string='Facilities', )
    project_percentage = fields.Float(string='Our Commission')
    image = fields.Binary(string='Image')
    description = fields.Text(string='Description')
    region = fields.Text(string='Region')
    project_image_ids = fields.One2many('real.estate.project.image', 'real_estate_project_id', string='Images')
    project_unit_type_ids = fields.One2many('real.estate.project.unit.type', 'real_estate_project_id',
                                            string='Unit Types')
    project_type_id = fields.Many2one('real.estate.project.type', string='Project Type')
    start_meter_price = fields.Float(string='Meter Price Starts At')
    project_presentation = fields.Binary('Project Presentation')
    deposit_percentage = fields.Float(string='Deposit')
    installments_period = fields.Integer(string='Installments Period')
    # address fields
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')

    project_latitude = fields.Float(string='Geo Latitude', digits=(16, 5))
    project_longitude = fields.Float(string='Geo Longitude', digits=(16, 5))
    project_localization = fields.Date(string='GeoLocation Date')
    code = fields.Char(string='Code', readonly=1, copy=False)

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('project.code')
        return super(RealEstateProject, self).create(vals)

    @api.model
    def _geo_localize(self, street='', zip='', city='', state='', country=''):
        geo_obj = self.env['base.geocoder']
        search = geo_obj.geo_query_address(street=street, zip=zip, city=city, state=state, country=country)
        result = geo_obj.geo_find(search, force_country=country)
        if result is None:
            search = geo_obj.geo_query_address(city=city, state=state, country=country)
            result = geo_obj.geo_find(search, force_country=country)
        return result

    def project_geo_localize(self):
        for project in self.with_context(lang='en_US'):
            result = project._geo_localize(street=project.street,
                                           zip=project.zip,
                                           city=project.city,
                                           state=project.state_id.name,
                                           country=project.country_id.name)
            if result is None:
                result = project._geo_localize(
                    city=project.city,
                    state=project.state_id.name,
                    country=project.country_id.name
                )

            if result:
                project.write({
                    'project_latitude': result[0],
                    'project_longitude': result[1],
                    'project_localization': fields.Date.context_today(project)
                })
        return True
