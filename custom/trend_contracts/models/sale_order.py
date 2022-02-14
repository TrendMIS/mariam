from string import Formatter

from num2words import num2words

from odoo import api, models, fields

DAYS = {
    "Saturday": "السبت",
    "Sunday": "الأحد",
    "Monday": "الإثنين",
    "Tuesday": "الثلاثاء",
    "Wednesday": "الأربعاء",
    "Thursday": "الخميس",
    "Friday": "الجمعة",
}


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    _description = "Sales order modification"

    # Contract Details
    unit_id = fields.Many2one("product.product", compute="_get_unit")
    project_id = fields.Many2one("real.estate.project", related="unit_id.real_estate_project_id")
    contract_partner_name = fields.Char()
    contract_partner_national_id = fields.Char()
    contract_partner_national_id_origin = fields.Char()
    contract_partner_address = fields.Char()
    contract_partner_mobile = fields.Char()
    unit_name = fields.Char(related="unit_id.name")
    unit_code = fields.Char(related="unit_id.unit_code")
    unit_area = fields.Float(related="unit_id.unit_area")
    unit_net_area = fields.Float(related="unit_id.unit_net_area")
    number_of_rooms = fields.Integer(related="unit_id.number_of_rooms")
    garden_area = fields.Char(related="unit_id.garden_area")
    unit_type = fields.Many2one(related="unit_id.unit_type")
    floor = fields.Char(related="unit_id.floor")
    full_unit_price_words = fields.Char(compute="_get_words")
    installment_amount_words = fields.Char(compute="_get_words")
    contract_signing_amount_words = fields.Char(compute="_get_words")
    today = fields.Char(compute="_get_date")
    date = fields.Date(compute="_get_date")
    report_type = fields.Many2one("contract.report.type")
    report_html = fields.Html()

    @api.depends("order_line")
    def _get_words(self):
        for record in self:
            record.full_unit_price_words = num2words(record.full_unit_price, lang="ar")
            record.contract_signing_amount_words = num2words(record.contract_signing_amount, lang="ar")
            record.installment_amount_words = num2words(record.installment_amount, lang="ar")

    @api.depends("order_line")
    def _get_unit(self):
        for sale in self:
            if not sale.order_line:
                sale.unit_id = False
                return
            sale.unit_id = sale.order_line[0].product_id

    @api.onchange("report_type")
    def onchange_report_type(self):
        if not self.report_type:
            self.report_html = ""
            return
        variables = self._get_variables(self.report_type.contract_html)
        self.report_html = self.report_type.contract_html.format(**variables)

    def print_contract(self):
        return self.env.ref('trend_contracts.action_contract_report').report_action(self)

    def _get_date(self):
        for record in self:
            record.today = DAYS[fields.Date.today().strftime("%A")]
            record.date = fields.Date.today()

    def _get_variables(self, contract_html):
        report_vars = [var for _, var, _, _ in Formatter().parse(contract_html) if var is not None]
        print(report_vars)
        return {var: getattr(self, var) for var in report_vars}
