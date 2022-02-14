from odoo import models, fields


class DesignFloor(models.Model):
    _name = 'design.floor'

    name = fields.Char(required=True)
    building_id = fields.Many2one("design.building")
    project_id = fields.Many2one(related="building_id.project_id")
    plan_id = fields.Many2one("design.plan")
    item_ids = fields.One2many('design.floor.item', "floor_id")


class DesignFloorItem(models.Model):
    _name = 'design.floor.item'
    floor_id = fields.Many2one("design.floor")
    item_id = fields.Many2one("design.plan.item", required=True)
    unit_id = fields.Many2one("product.product", required=True)
