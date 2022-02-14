# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    team_history_count = fields.Integer(string="History Count", compute="get_team_history_count")

    def get_team_history_count(self):
        for team in self:
            team.team_history_count = self.env['crm.team.history'].sudo().search_count([('team_id', '=', team.id)])

    def action_open_team_history(self):
        for team in self:
            team_history_objects = self.env['crm.team.history'].sudo().search([('team_id', '=', team.id)])
            form_view_id = self.env.ref('trend_realestate_lead.crm_team_history_form_view')
            tree_view_id = self.env.ref('trend_realestate_lead.crm_team_history_tree_view')
            return {
                'name': _('Team History'),
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'res_model': 'crm.team.history',
                'views': [(tree_view_id.id, 'tree'), (form_view_id.id, 'form')],
                'view_id': tree_view_id.id,
                'target': 'current',
                'context': {'create': 0, 'edit': 0},
                'domain': [('id', 'in', team_history_objects.ids)],
            }

    def write(self, vals):
        for team in self:
            # add history for team leader
            if 'user_id' in vals:
                if team.user_id and vals['user_id'] != False:
                    created_history = self.env['crm.team.history'].create({
                        "name": "Change Team Leader",
                        "team_id": team.id,
                        "change_from_user_id": team.user_id.id,
                        "change_to_user_id": vals["user_id"],
                        "date": fields.Date.today(),
                    })
                elif team.user_id and vals['user_id'] == False:
                    created_history = self.env['crm.team.history'].create({
                        "name": "Remove Team Leader",
                        "team_id": team.id,
                        "change_from_user_id": team.user_id.id,
                        "change_to_user_id": vals["user_id"],
                        "date": fields.Date.today(),
                    })

            # change in members
            if 'member_ids' in vals:
                new_user_ids = []
                # Add new member in team
                if len(vals['member_ids']) <= len(team.member_ids.ids) and team.member_ids.ids:
                    if vals['member_ids'][0][2]:
                        new_user_ids = list(set(vals['member_ids'][0][2]) - set(team.member_ids.ids))

                # Add first member
                elif len(vals['member_ids']) > len(team.member_ids.ids) and not team.member_ids.ids:
                    new_user_ids = vals['member_ids'][0][2]

                for member_list in vals['member_ids']:
                    if member_list and len(member_list) > 0 and member_list[0] == 3:
                        created_history = self.env['crm.team.history'].create({
                            "name": "Remove Member",
                            "team_id": team.id,
                            "change_from_user_id": member_list[1],
                            "date": fields.Date.today(),
                        })

                for user_id in new_user_ids:
                    created_history = self.env['crm.team.history'].create({
                        "name": "Add Member",
                        "team_id": team.id,
                        "change_from_user_id": user_id,
                        "date": fields.Date.today(),
                    })
                    user_crm_leads = self.env['crm.lead'].sudo().search([('user_id', '=', user_id)])
                    for lead in user_crm_leads:
                        lead.write({'team_id': self.id})

        return super(CrmTeam, self).write(vals)
