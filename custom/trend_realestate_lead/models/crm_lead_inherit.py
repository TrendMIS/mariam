# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

from html2text import HTML2Text


class Lead(models.Model):
    _inherit = 'crm.lead'
    _order = 'write_date DESC'

    product_ids = fields.Many2many('product.product',
                                   'product_lead_rel', 'lead_id', 'product_id',
                                   copy=False, string='Interested Units',
                                   domain=[('is_real_estate_unit', '=', True)])
    budget_from = fields.Float(string='From')
    budget_to = fields.Float(string='To')
    area_from = fields.Float(string='From')
    area_to = fields.Float(string='To')
    status = fields.Many2one(comodel_name='status.type', track_visibility='onchange')
    last_log_comment = fields.Html(string='Last Comment', compute='get_lead_last_log_comment')
    shared_with_user_id = fields.Many2one("res.users", string="Shared With")
    partner_leads_count = fields.Integer(string="Customer Leads", compute='get_partner_values')
    partner_duplicate = fields.Boolean(string='Duplicate', compute='get_partner_values')
    stage_type = fields.Selection(related='stage_id.stage_type', string='Stage Type')
    team_leader_user_id = fields.Many2one("res.users", string="Team Leader")
    lead_invoices_count = fields.Integer(string="Lead Invoices", compute='get_lead_invoices_count')
    unit_number = fields.Char(string='Unit Number')
    contract_name = fields.Char(string='Contract Name')

    last_stage_id = fields.Many2one('crm.stage', string='Last Stage')
    lead_history_ids = fields.One2many(comodel_name="crm.lead.history", inverse_name="lead_id", string="",
                                       required=False, )
    creation_date = fields.Date(string="Creation Date")
    broker_id = fields.Many2one("res.partner", string="Broker", domain=[('is_broker', '=', True)])
    referred = fields.Many2one('res.users', string='Referred By')
    recommended_by_id = fields.Many2one('res.partner')
    mobile = fields.Char(related="partner_id.mobile", readonly=True)
    phone = fields.Char(related="partner_id.phone", readonly=True)
    admin_tags_ids = fields.Many2many('crm.admin.tag', string="Admin Tag",
                                      groups="trend_realestate_access_rights.res_group_real_estate_sales_team_leader")
    call_center = fields.Boolean(string="Call Center")
    customer_code = fields.Char(related="partner_id.customer_code")
    branch = fields.Selection(selection=[('thawra', 'Thawra'), ('new_cairo', 'New Cairo'), ])

    def write(self, values):
        re_assign_stage_object = self.env['crm.stage'].search([('stage_type', '=', 're_assign')], limit=1)
        for lead in self:
            user_team_object = self.env['crm.team']._get_default_team_id(user_id=lead.user_id.id)
            if 'user_id' in values:
                lead_mail_activity_objects = self.env['mail.activity'].sudo().search(
                    [('res_id', '=', lead.id), ('user_id', '!=', values['user_id'])])

                for activity_object in lead_mail_activity_objects:
                    activity_object.sudo().write({'user_id': values['user_id']})

                # set stage to re-assign when change salesperson
                # if lead.stage_id.stage_type != 'fresh' and re_assign_stage_object and lead.user_id != user_team_object.user_id:
                #     values['stage_id'] = re_assign_stage_object.id

            # set value in team leader when mark lead as won
            if 'stage_id' in values and lead.user_id:
                values['last_stage_id'] = lead.stage_id.id
                lead_stage_object = self.env['crm.stage'].sudo().browse(values['stage_id'])
                if lead_stage_object.stage_type == 'won':
                    values['contract_name'] = lead.partner_id.display_name if lead.partner_id else ''
                    if user_team_object.user_id:
                        values['team_leader_user_id'] = user_team_object.user_id.id
        return super(Lead, self).write(values)

    @api.depends('partner_id')
    def get_partner_values(self):
        for lead in self:
            if lead.id:
                partner_leads_count = self.env['crm.lead'].sudo().search_count(
                    [('partner_id', '=', lead.partner_id.id), ('partner_id', '!=', False), ('id', '!=', lead.id)])
                lead.partner_leads_count = partner_leads_count
                if partner_leads_count > 0:
                    lead.partner_duplicate = True
                else:
                    lead.partner_duplicate = False
            else:
                lead.partner_duplicate = False
                lead.partner_leads_count = 0

    def open_partner_leads(self):
        for lead in self:
            partner_leads_objects = self.env['crm.lead'].sudo().search(
                [('partner_id', '=', lead.partner_id.id), ('id', '!=', lead.id)])
            form_view_id = self.env.ref('crm.crm_lead_view_form')
            tree_view_id = self.env.ref('crm.crm_case_tree_view_oppor')
            return {
                'name': _('Customer Leads'),
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'res_model': 'crm.lead',
                'views': [(tree_view_id.id, 'tree'), (form_view_id.id, 'form')],
                'view_id': tree_view_id.id,
                'target': 'current',
                'domain': [('id', 'in', partner_leads_objects.ids)],
            }

    def get_lead_last_log_comment(self):
        html = HTML2Text()
        for lead in self:
            last_message_object = self.env['mail.message'].sudo().search([('id', 'in', lead.message_ids.ids)],
                                                                         order='create_date DESC', limit=1)
            if last_message_object:
                lead.last_log_comment = html.handle(last_message_object.body)
            else:
                lead.last_log_comment = ''

    def action_assign_user(self):
        form_view_id = self.env.ref('trend_realestate_lead.assign_multi_lead_user_wizard_form_view').id
        return {
            'name': _('Assign Salesperson'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': form_view_id,
            'res_model': 'assign.multi.lead.user.wizard',
            'target': 'new',
            'context': {'multi_lead_ids': self.ids, }
        }

    def action_create_lead_invoice(self):
        for lead in self:
            lead_move_objects = self.env['account.move'].search(
                [('crm_lead_id', '=', lead.id)])
            form_view_id = self.env.ref('account.view_move_form')
            tree_view_id = self.env.ref('account.view_invoice_tree')
            commission_product_id = int(self.env['ir.config_parameter'].sudo().get_param('commission_product_id'))
            commission_product_object = self.env['product.product'].browse(commission_product_id)
            journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
            account_id = journal.default_credit_account_id.id

            return {
                'name': _('Lead Invoices'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form,tree',
                'res_model': 'account.move',
                'views': [(form_view_id.id, 'form'), (tree_view_id.id, 'tree'), ],
                'view_id': tree_view_id.id,
                'target': 'current',
                'domain': [('id', 'in', lead_move_objects.ids)],
                'context': {'default_partner_id': lead.name.developer_id.id, 'default_user_id': lead.user_id.id,
                            'default_crm_lead_id': lead.id, 'default_date_invoice': fields.Date.today(),
                            'default_invoice_origin': lead.name.name, 'default_type': 'out_invoice',
                            'default_journal_type': 'sale',
                            }
            }

    def get_lead_invoices_count(self):
        for lead in self:
            lead.lead_invoices_count = self.env['account.move'].search_count(
                [('crm_lead_id', '=', lead.id)])

    def action_open_lead_invoices(self):
        for lead in self:
            lead_invoice_objects = self.env['account.move'].search(
                [('crm_lead_id', '=', lead.id)])
            form_view_id = self.env.ref('account.view_move_form')
            tree_view_id = self.env.ref('account.view_invoice_tree')
            return {
                'name': _('Lead Invoices'),
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'res_model': 'account.move',
                'views': [(tree_view_id.id, 'tree'), (form_view_id.id, 'form'), ],
                'view_id': tree_view_id.id,
                'target': 'current',
                'domain': [('id', 'in', lead_invoice_objects.ids)],
            }

    @api.model
    def create(self, vals):
        # set up context used to find the lead's Sales Team which is needed
        # to correctly set the default stage_id
        context = dict(self._context or {})
        if vals.get('type') and not self._context.get('default_type'):
            context['default_type'] = vals.get('type')
        if vals.get('team_id') and not self._context.get('default_team_id'):
            context['default_team_id'] = vals.get('team_id')

        if vals.get('user_id') and 'date_open' not in vals:
            vals['date_open'] = fields.Datetime.now()

        if context.get('default_partner_id') and not vals.get('email_from'):
            partner = self.env['res.partner'].browse(context['default_partner_id'])
            vals['email_from'] = partner.email

        if context.get('default_partner_id') and not vals.get('mobile'):
            partner = self.env['res.partner'].browse(context['default_partner_id'])
            vals['mobile'] = partner.mobile

        # context: no_log, because subtype already handle this
        return super(Lead, self.with_context(context, mail_create_nolog=True)).create(vals)

    def _should_update_probability(self, vals):
        """
        We override this method to stop automatic changing of probabilities
        """
        return False

    def cancel_activities(self):
        for lead in self:
            domain = [
                ('res_model', '=', 'crm.lead'),
                ('res_id', '=', lead.id),
            ]
            activities = self.env['mail.activity'].search(domain)
            activities.unlink()

    def action_set_won_rainbowman(self):
        super().action_set_won_rainbowman()
        result = self.call_wizard()
        if result:
            return result

    def call_wizard(self):
        return {
            'name': 'adding unit to lead',
            'res_model': 'available.units.wizard',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }

    def action_new_quotation(self):
        action = super().action_new_quotation()
        print(action)
        action['context'].update({
            'default_order_line': [(0, 0, {"product_id": product.id, "price_unit": product.list_price}) for product in
                                   self.product_ids],
        })
        return action


class StatusType(models.Model):
    _name = 'status.type'

    name = fields.Char()
