# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    unit_code = fields.Char()
    block_id = fields.Many2one("realestate.unit.block")
    view_id = fields.Many2one("realestate.unit.view")
    finish_id = fields.Many2one("realestate.unit.finish")
    has_garden = fields.Boolean()
    garden_area = fields.Char()
    garden_price = fields.Float()
    number_of_rooms = fields.Integer()
    number_of_bathrooms = fields.Integer()
    is_locked = fields.Boolean()
    unit_type = fields.Many2one('realestate.unit.type')

    def change_lock_status(self):
        for unit in self:
            unit.with_context({"allow_write": True}).is_locked = not unit.is_locked

    def write(self, vals):
        super().write(vals)
        if self.env.context.get("allow_write"):
            return
        for record in self:
            if record.is_locked:
                raise ValidationError("You can't edit a locked unit")


class UnitBlock(models.Model):
    _name = "realestate.unit.block"
    _description = "Realestate unit info"
    _rec_name = "number"

    number = fields.Char(required=True)
    project_id = fields.Many2one('real.estate.project', string='Real Estate Project', required=True)


class UnitView(models.Model):
    _name = "realestate.unit.view"
    _description = "Realestate unit view"

    name = fields.Char(required=True)
    project_id = fields.Many2one('real.estate.project', string='Real Estate Project')


class UnitFinish(models.Model):
    _name = "realestate.unit.finish"
    _description = "Realestate unit finish status"

    name = fields.Char(required=True)


class UnitType(models.Model):
    _name = "realestate.unit.type"

    name = fields.Char(required=True)
