import math
from datetime import datetime, time
import pytz

from odoo import api, fields, models


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    def _get_default_deadline_time(self):
        user_timezone = pytz.timezone(self.env.user.tz or 'Africa/Cairo')
        now = datetime.now(tz=user_timezone)
        return now.hour + now.minute / 60

    def _get_default_reminder(self):
        try:
            return self.env.ref("trend_mail_activity_reminder.alarm_one_minute")
        except ValueError:
            return False

    deadline = fields.Datetime(string='Deadline', compute='_compute_deadline', compute_sudo=True)
    time_deadline = fields.Float(string='Schedule Time', default=_get_default_deadline_time, required=True)
    create_reminder = fields.Boolean()
    reminder_alarm = fields.Many2one("calendar.alarm", default=_get_default_reminder)
    event_id = fields.Many2one("calendar.event")

    @staticmethod
    def convert_float_to_time(float_time):
        hour = int(math.floor(float_time))
        minute = int(round((float_time % 1) * 60))
        return time(hour=hour, minute=minute)

    @api.depends('user_id.tz', 'date_deadline', 'time_deadline')
    def _compute_deadline(self):
        for activity in self:
            time_deadline = self.convert_float_to_time(activity.time_deadline)
            deadline = datetime.combine(activity.date_deadline, time_deadline)
            user_tz = pytz.timezone(self.env.user.tz or 'Africa/Cairo')
            activity.deadline = user_tz.localize(deadline).astimezone(pytz.utc).replace(tzinfo=None)

    @api.model
    def create(self, vals):
        activity = super().create(vals)
        if activity.create_reminder:
            activity.schedule_event()
        return activity

    def write(self, vals):
        for activity in self:
            super().write(vals)
            if activity.create_reminder:
                check_fields = ["date_deadline", "time_deadline", "create_reminder", "reminder_alarm"]
                if [field for field in check_fields if field in vals]:
                    activity.event_id.unlink()
                    activity.schedule_event()

    def schedule_event(self):
        event = self.env['calendar.event'].sudo().create({
            # 'state': 'open',
            'name': f"{self.res_name} {self.summary or ''}",

            'start': fields.Datetime.to_string(self.deadline),
            'start_date': fields.Date.to_string(self.deadline.date()),
            # 'start_datetime': fields.Datetime.to_string(self.deadline),

            'stop': fields.Datetime.to_string(self.deadline),
            'stop_date': fields.Date.to_string(self.deadline.date()),
            # 'stop_datetime': fields.Datetime.to_string(self.deadline),

            'description': f"""
                <b><a href="/web#id={self.res_id}&model={self.res_model}&view_type=form">Related Record</a></b>
                <br/>
                {self.note}
            """,
            'res_id': self.res_id,
            'res_model': self.res_model,
            'alarm_ids': [(4, self.reminder_alarm.id)],
        })
        self.event_id = event
