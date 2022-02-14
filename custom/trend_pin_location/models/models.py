# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests
from collections import defaultdict


class Lead(models.Model):
    _inherit = 'crm.lead'

    lat = fields.Char()
    lng = fields.Char()


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    def _action_done(self, feedback=False, attachment_ids=None):
        messages = self.env['mail.message']
        next_activities_values = []

        attachments = self.env['ir.attachment'].search_read([
            ('res_model', '=', self._name),
            ('res_id', 'in', self.ids),
        ], ['id', 'res_id'])

        activity_attachments = defaultdict(list)
        for attachment in attachments:
            activity_id = attachment['res_id']
            activity_attachments[activity_id].append(attachment['id'])

        for activity in self:
            if activity.force_next:
                Activity = self.env['mail.activity'].with_context(
                    activity_previous_deadline=activity.date_deadline)
                vals = Activity.default_get(Activity.fields_get())

                vals.update({
                    'previous_activity_type_id': activity.activity_type_id.id,
                    'res_id': activity.res_id,
                    'res_model': activity.res_model,
                    'res_model_id': self.env['ir.model']._get(activity.res_model).id,
                })
                virtual_activity = Activity.new(vals)
                virtual_activity._onchange_previous_activity_type_id()
                virtual_activity._onchange_activity_type_id()
                next_activities_values.append(virtual_activity._convert_to_write(virtual_activity._cache))
            record = self.env[activity.res_model].browse(activity.res_id)
            if self.activity_type_id.pin_location:
                res = requests.get('https://ipinfo.io/')
                data = res.json()
                location = data['loc'].split(',')
                lat = location[0]
                lag = location[1]

                if not feedback:
                    content = 'Pin Location 👇' + '\n' + 'https://www.google.com/maps/search/?api=1&query={}+{}'.format(
                        lat, lag)
                else:
                    content = feedback + '\n' + 'Pin Location 👇' + '\n' + 'https://www.google.com/maps/search/?api=1&query={}+{}'.format(
                        lat, lag)
                record.message_post_with_view(
                    'mail.message_activity_done',
                    values={
                        'activity': activity,
                        'feedback': content,
                        'display_assignee': activity.user_id != self.env.user
                    },
                    subtype_id=self.env['ir.model.data'].xmlid_to_res_id('mail.mt_activities'),
                    mail_activity_type_id=activity.activity_type_id.id,
                    attachment_ids=[(4, attachment_id) for attachment_id in attachment_ids] if attachment_ids else [],
                )
            else:
                record.message_post_with_view(
                    'mail.message_activity_done',
                    values={
                        'activity': activity,
                        'feedback': feedback,
                        'display_assignee': activity.user_id != self.env.user
                    },
                    subtype_id=self.env['ir.model.data'].xmlid_to_res_id('mail.mt_activities'),
                    mail_activity_type_id=activity.activity_type_id.id,
                    attachment_ids=[(4, attachment_id) for attachment_id in attachment_ids] if attachment_ids else [],
                )
            activity_message = record.message_ids[0]
            message_attachments = self.env['ir.attachment'].browse(activity_attachments[activity.id])
            if message_attachments:
                message_attachments.write({
                    'res_id': activity_message.id,
                    'res_model': activity_message._name,
                })
                activity_message.attachment_ids = message_attachments
            messages |= activity_message

        next_activities = self.env['mail.activity'].create(next_activities_values)
        self.unlink()

        return messages, next_activities
