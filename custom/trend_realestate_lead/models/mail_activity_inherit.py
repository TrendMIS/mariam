# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import timedelta, datetime


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    schedule_activity_date = fields.Datetime(string='Schedule Time')

    @api.onchange('date_deadline')
    def set_schedule_date(self):
        for activity in self:
            if activity.date_deadline:
                activity.schedule_activity_date = fields.Datetime.to_string(
                    datetime.combine(activity.date_deadline, fields.Datetime.now().time()))
