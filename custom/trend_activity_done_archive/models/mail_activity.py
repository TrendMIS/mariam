from odoo import models, fields


class MailActivityArchive(models.Model):
    _name = 'mail.activity.archive'

    res_model_id = fields.Many2one('ir.model', 'Document Model', ondelete='cascade', required=True)
    res_model = fields.Char(related='res_model_id.model', compute_sudo=True, store=True, readonly=True)
    res_id = fields.Many2oneReference(string='Related Document ID', required=True, model_field='res_model')
    res_name = fields.Char('Document Name')
    # activity
    activity_type_id = fields.Many2one('mail.activity.type', string='Activity Type')
    activity_category = fields.Selection(related='activity_type_id.category', readonly=True)
    activity_decoration = fields.Selection(related='activity_type_id.decoration_type', readonly=True)
    summary = fields.Char('Summary')
    note = fields.Html('Note', sanitize_style=True)
    date_deadline = fields.Date('Due Date', index=True, required=True, default=fields.Date.context_today)
    automated = fields.Boolean('Automated activity', readonly=True,
                               help='Indicates this activity has been created automatically and not by any user.')
    user_id = fields.Many2one('res.users', 'Assigned to', index=True, required=True)
    previous_activity_type_id = fields.Many2one('mail.activity.type', string='Previous Activity Type', readonly=True)
    lead_id = fields.Many2one("crm.lead", readonly=True, string="Project")
    team_id = fields.Many2one(related="lead_id.team_id", string="Team", store=True)
    partner_id = fields.Many2one(related="lead_id.partner_id", string="Customer", store=True)
    stage_id = fields.Many2one(related="lead_id.stage_id", store=True)
    campaign_id = fields.Many2one(related="lead_id.campaign_id", store=True)
    source_id = fields.Many2one(related="lead_id.source_id", store=True)
    medium_id = fields.Many2one(related="lead_id.medium_id", store=True)
    lead_creation_date = fields.Datetime(related="lead_id.create_date")


class MailActivity(models.Model):
    _inherit = 'mail.activity'
    team_id = fields.Many2one("crm.team", string="Team", store=True)

    def _action_done(self, feedback=False, attachment_ids=None):
        for activity in self:
            if activity.res_model != 'crm.lead':
                continue
            lead = self.env["crm.lead"].browse(activity.res_id)
            self.env['mail.activity.archive'].sudo().create({
                "res_model_id": activity.res_model_id.id,
                "res_id": activity.res_id,
                "res_name": activity.res_name,
                "activity_type_id": activity.activity_type_id.id,
                "summary": activity.summary,
                "note": activity.note,
                "date_deadline": activity.date_deadline,
                "automated": activity.automated,
                "user_id": activity.user_id.id,
                "previous_activity_type_id": activity.previous_activity_type_id.id,
                "lead_id": lead.id,
                "lead_creation_date": lead.create_date,
                "team_id": activity.team_id
            })
        return super()._action_done(feedback=feedback, attachment_ids=attachment_ids)
