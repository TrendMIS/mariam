from odoo import models, fields


class DesignBuilding(models.Model):
    _name = 'design.building'

    name = fields.Char(required=True)
    project_id = fields.Many2one("real.estate.project")
    floor_ids = fields.One2many("design.floor", "building_id")
    fields_ids = fields.Many2many("ir.model.fields")

    def view_plan(self):
        return {
            'name': 'Go to Plan Design',
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': f'/realestate-design/{self.id}'
        }
