# -*-	coding:	utf-8	-*-

from odoo import models, api, fields, _


class BrokerCommissionProgram(models.Model):
    _name = "broker.commission.program"
    _description = "Broker Commission Program"
    _inherit = "mail.thread"

    name = fields.Char(required=True)
    applied_on = fields.Selection(string="", selection=[('broker', 'Broker'),
                                                        ('broker_salesman', 'Broker Salesman')],
                                  required=True, default='broker')
    line_ids = fields.One2many(comodel_name="broker.commission.program.line", inverse_name="broker_program_id",
                               string="Targets")


class BrokerCommissionProgramLine(models.Model):
    _name = "broker.commission.program.line"

    target_from = fields.Float(string="", required=False, )
    target_to = fields.Float(string="", required=False, )
    commission_percentage = fields.Float(string="", required=False, )
    broker_program_id = fields.Many2one(comodel_name="broker.commission.program", required=True,
                                        ondelete="cascade")
