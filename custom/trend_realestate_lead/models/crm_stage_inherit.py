# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class CrmStage(models.Model):
    _inherit = 'crm.stage'

    stage_type = fields.Selection([('fresh', 'Fresh'), ('re_assign', 'Re-Assign'), ('won', 'Won')], string='Stage Type')
