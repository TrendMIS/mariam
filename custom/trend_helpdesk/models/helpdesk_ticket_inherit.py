# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    sale_id = fields.Many2one('sale.order')
    project = fields.Char(readonly=True)
    ticket_note = fields.Boolean(compute='_read_assigned_ticket')
    read_ticket = fields.Boolean(default=False, readonly=True)

    @api.onchange('partner_id')
    def _get_customer_sales_order(self):
        for rec in self:
            return {'domain': {'sale_id': [('partner_id', '=', rec.partner_id.id)]}}

    @api.onchange('sale_id')
    def get_sales_projects(self):
        if self.sale_id:
            for rec in self:
                sale = self.env["sale.order"].search([('id', '=', rec.sale_id.id)])
                self.project = sale.project_id.name

    def _read_assigned_ticket(self):
        for rec in self:
            if not rec.read_ticket:
                if rec.user_id.id == self.env.user.id:
                    self.read_ticket = True
                    self.message_post(body=f"{self.env.user.name} has read the ticket")
            rec.ticket_note = True
