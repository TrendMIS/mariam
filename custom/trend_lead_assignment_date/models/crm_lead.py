# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    first_assignee_readonly = fields.Boolean()
    another_date_open = fields.Datetime()

    def write(self, vals):
        if vals.get('user_id'):
            user = self.env['res.users'].browse(vals.get('user_id'))
            if user.is_salesperson and not self.first_assignee_readonly:
                vals['first_assignee_id'] = vals.get('user_id')
                vals['first_assignee_readonly'] = True
                vals['another_date_open'] = fields.Datetime.now()
        return super().write(vals)

    @api.model
    def create(self, values):
        res = super(CrmLead, self).create(values)
        user = self.env['res.users'].browse(values.get('user_id'))
        if user.is_salesperson:
            res.first_assignee_id = values['user_id']
            res.first_assignee_readonly = True
            res.another_date_open = fields.Datetime.now()
        return res

    @api.depends('another_date_open')
    def _compute_date_open(self):
        for lead in self:
            lead.date_open = lead.another_date_open if lead.first_assignee_id else False
