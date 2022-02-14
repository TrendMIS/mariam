from odoo import models, fields


class DesignPlan(models.Model):
    _name = 'design.plan'

    name = fields.Char(required=True)
    project_id = fields.Many2one("real.estate.project", required=True)
    image = fields.Binary(required=True)
    item_ids = fields.One2many('design.plan.item', "plan_id")


class DesignPlanItem(models.Model):
    _name = 'design.plan.item'

    name = fields.Char(required=True)
    coordinates = fields.Text(required=True)
    plan_id = fields.Many2one('design.plan')
