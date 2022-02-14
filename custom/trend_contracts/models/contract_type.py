from odoo import fields, models


class ContractType(models.Model):

    _name = "contract.report.type"

    name = fields.Char()
    project_id = fields.Many2one('real.estate.project')
    contract_html = fields.Html()

