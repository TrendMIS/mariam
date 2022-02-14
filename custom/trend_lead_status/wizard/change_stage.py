# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ChangeStageWizard(models.TransientModel):
    _name = 'change.stage.wizard'
    _description = 'Change Stage Wizard'

    crm_stage_id = fields.Many2one(comodel_name='crm.stage', string='Stage', required=True)
    status_ids = fields.Many2many(comodel_name="status.type", related='crm_stage_id.status_ids')
    status_type_id = fields.Many2one(comodel_name='status.type', string='Status Type', required=True)

    def confirm(self):
        lead = self.env['crm.lead'].browse(self.env.context.get('active_ids'))
        lead.write({'stage_id': self.crm_stage_id.id, 'status': self.status_type_id.id})
