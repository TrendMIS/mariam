# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = 'res.partner'

    birth_date = fields.Date(string='Birth Date')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    number_of_children = fields.Integer(string='Number Of Children')
    club_membership = fields.Text(string='Club Membership')
    educational_degree = fields.Char(string='Educational Degree')
    developer = fields.Boolean(string='Is A Developer')
    formal_company_name = fields.Char(string='Formal Company Name')
    is_broker = fields.Boolean(string="Is A Broker")
    customer = fields.Boolean(string="Is A Customer")
    vendor = fields.Boolean(string="Is A Vendor")
    partner_code = fields.Char(string='Code', readonly=0, copy=False)
    customer_code = fields.Char(string='Customer Code')

    _sql_constraints = [("UniqueEmail", "UNIQUE(email)", "Email already exists"),
                        ("UniqueCustomerCode", "UNIQUE(customer_code)", "code is already used")]

    @api.model
    def create(self, vals):
        if 'customer' in vals and vals['customer'] == True:
            vals['partner_code'] = self.env['ir.sequence'].next_by_code('customer.code')

        if 'vendor' in vals and vals['vendor'] == True:
            vals['partner_code'] = self.env['ir.sequence'].next_by_code('vendor.code')

        if 'is_broker' in vals and vals['is_broker'] == True:
            vals['partner_code'] = self.env['ir.sequence'].next_by_code('broker.code')
        return super(ResPartner, self).create(vals)

    @api.constrains('mobile', 'phone')
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
            numbers = tuple(numbers)
            if not numbers:
                return True
            query = """
            SELECT id FROM  res_partner 
            WHERE id != %s
            AND (RIGHT(mobile, 10) in %s OR RIGHT(phone, 10) in %s) ;
            """
            self._cr.execute(query, (partner.id, numbers, numbers))
            partner_objects = self._cr.fetchall()
            if partner_objects:
                raise ValidationError(_('Mobile and phone must be unique value.'))

    @api.constrains('email')
    def check_email_value(self):
        for partner in self:
            if not partner.email:
                return True
            partners = self.search([('id', '!=', partner.id), ('email', 'ilike', partner.email)])
            if partners:
                raise ValidationError(_('Email is already exists'))

    @api.constrains('birth_date')
    def check_birth_date(self):
        for partner in self:
            if partner.birth_date and partner.birth_date >= fields.Date.today():
                raise ValidationError(_('Birth date must be less than today.'))
