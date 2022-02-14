# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    lead_ids = fields.Many2many('crm.lead', 'product_lead_rel', 'product_id', 'lead_id',
                                copy=False, string='Interested Leads')
    phase_id = fields.Many2one('unit.phase', string="Unit Phase")

    def open_unit_leads(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'name': 'Leads',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('id', 'in', self.lead_ids.ids)],

        }


class UnitPhase(models.Model):
    _name = 'unit.phase'

    name = fields.Char()
