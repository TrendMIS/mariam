# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProjectFacility(models.Model):
    _name = 'project.facility'
    _description = 'Project Facility'

    name = fields.Char(string='Name', required=True)
