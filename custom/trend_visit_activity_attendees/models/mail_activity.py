from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "mail.activity"

    attendees_ids = fields.Many2many('res.users')
    visit_type = fields.Many2one("visit.activity.type")

    def activity_format(self):
        activities = super().activity_format()
        for activity in activities:
            attendees = self.env['res.users'].browse(activity['attendees_ids'])
            activity['attendees_ids'] = attendees.read(['id', 'name'])
        return activities


class VisitActivityType(models.Model):
    _name = "visit.activity.type"

    name = fields.Char()
