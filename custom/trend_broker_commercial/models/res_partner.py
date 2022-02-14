# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    broker_commercial_register = fields.Char()

    _sql_constraints = [("UniqueCommercialRegister", "UNIQUE(broker_commercial_register)",
                         "Broker commercial register already exists")]
