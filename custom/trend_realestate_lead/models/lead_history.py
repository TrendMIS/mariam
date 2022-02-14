# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class LeadHistory(models.Model):
    _name = 'crm.lead.history'
    _rec_name = 'author'

    author = fields.Char(string="Author", required=True)
    comment = fields.Text(string="Comment")
    date = fields.Date(required=True)
    lead_id = fields.Many2one(comodel_name="crm.lead", required=True, ondelete="cascade")
