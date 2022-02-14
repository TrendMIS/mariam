from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class DashboardEmail(models.Model):
    _name = 'is.dashboard.email'
    _description = "Dashboard Email"
    _inherit = ['mail.thread']
    _inherits = {'ir.cron': 'cron_id'}

    active = fields.Boolean(default=True)
    cron_id_active = fields.Boolean(related="cron_id.active", default=True, readonly=False)
    cron_id = fields.Many2one(string="Schedule", comodel_name='ir.cron', required=True, ondelete="restrict")

    subject = fields.Char(string="Subject", required=True)
    user_id = fields.Many2one('res.users', 'From', default=lambda self: self._uid)
    to_partner_ids = fields.Many2many('res.partner', string="To")

    dashboard_id = fields.Many2one(comodel_name="is.dashboard", string="Dashboard")

    preview = fields.Html(compute="compute_preview")
    unsupported_tiles = fields.Boolean(compute="compute_preview")

    @api.model
    def default_get(self, default_fields):
        res = super(DashboardEmail, self).default_get(default_fields)
        if 'model_id' in default_fields:
            res['model_id'] = self.env.ref('dashboard_widgets.model_is_dashboard_email').id
        if 'model' in default_fields:
            res['model'] = 'dashboard_widgets.model_is_dashboard_email'
        if 'interval_type' in default_fields:
            res['interval_type'] = 'weeks'
        if 'state' in default_fields:
            res['state'] = 'code'
        if 'active' in default_fields:
            res['active'] = True
        return res

    @api.model
    def create(self, vals):
        res = super(DashboardEmail, self).create(vals)
        res.cron_id.code = "env['is.dashboard.email'].browse({}).action_send()".format(res.id)
        res.cron_id.numbercall = -1
        return res

    @api.onchange('subject')
    def onchange_subject(self):
        for rec in self:
            rec.name = "Email Schedule: {}".format(rec.subject or "")

    def action_send_composer(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('dashboard_widgets', 'email_template_dashboard')[1]
        except ValueError:
            template_id = False
        ctx = {
            'default_model': 'is.dashboard.email',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'force_email': False
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'target': 'new',
            'context': ctx,
        }

    def action_send(self):
        for rec in self:
            template = self.env.ref('dashboard_widgets.email_template_dashboard')
            template.send_mail(rec.id, force_send=False, raise_exception=True) #, email_values={'email_to': user.email, 'subject': subject})

    @api.depends(
        'name',
        'dashboard_id',
    )
    def compute_preview(self):
        for rec in self:
            not_supported_type = [
                'line_break',
                'graph',
                'embed_iframe_url',
                'embed_iframe_html',
            ]
            tiles = rec.dashboard_id.with_context(dashboard_id=rec.dashboard_id.id).widget_ids.filtered(lambda t: t.display_mode not in not_supported_type)
            rec.unsupported_tiles = rec.dashboard_id.widget_ids.filtered(lambda t: t.display_mode in not_supported_type)

            if not tiles:
                rec.preview = "Please select a dashboard"
                continue

            rows = []
            max_y = max(tiles.mapped('pos_y'))
            for y in range(max_y + 1):
                items = tiles.filtered(lambda t: t.pos_y == y)
                if items:
                    rows.append(items)

            rec.preview = self.env['ir.qweb'].render('dashboard_widgets.dashboard_email', values={
                'dashboard': rec,
                'rows': rows,
            })

            # items = rec.dashboard_ids.with_context(scheduled_email_id=rec.id)
            # items._compute_kanban_class_count()  # Fixes cache key error
            # items = sorted(items, key=lambda item: item.sequence_email)
            # rec.preview = self.env['ir.qweb'].render('dashboard_widgets.dashboard_email', values={
            #     'dashboard': rec,
            #     'items': items,
            # })
