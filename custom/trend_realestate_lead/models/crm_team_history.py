# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class CrmTeamHistory(models.Model):
    _name = 'crm.team.history'
    _description = 'Team History'

    name = fields.Char(string='Description', required=True)
    team_id = fields.Many2one("crm.team", string="Team", ondelete="cascade")
    change_from_user_id = fields.Many2one("res.users", string="From")
    change_to_user_id = fields.Many2one("res.users", string="To")
    date = fields.Date(string="Date")
