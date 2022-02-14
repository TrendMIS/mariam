# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MailActivityType(models.Model):
    _inherit = 'mail.activity.type'

    pin_location = fields.Boolean(string='Pin Location', required=False)
