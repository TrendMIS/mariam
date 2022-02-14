from odoo import models, fields


class MailActivityType(models.Model):
    _inherit = 'mail.activity.type'

    sms_template_id = fields.Many2one("sms.template")


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    def _action_done(self, feedback=False, attachment_ids=None):
        for activity in self:
            sms_template = activity.activity_type_id and activity.activity_type_id.sudo().sms_template_id
            if sms_template and activity.res_model == 'crm.lead':
                record = self.env[activity.res_model].browse(activity.res_id)
                record._message_sms_with_template(
                    template=sms_template,
                    partner_ids=record.partner_id.ids,
                    put_in_queue=False
                )
        return super()._action_done(feedback=feedback, attachment_ids=attachment_ids)
