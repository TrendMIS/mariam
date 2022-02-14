from odoo import models, fields


class MailActivityMixin(models.AbstractModel):
    _inherit = 'mail.activity.mixin'

    activity_date_deadline = fields.Date(store=True)
