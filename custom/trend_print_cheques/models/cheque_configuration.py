from num2words import num2words
from odoo import api, fields, models


class ChequeConfiguration(models.Model):
    _name = 'cheque.configuration'
    _rec_name = 'name'
    _description = 'Cheque Configuration'

    name = fields.Char()

    cheque_img = fields.Binary(string="Cheque Image", )

    font_size = fields.Integer(string="Font Size", default=20)

    date_margin_top = fields.Integer(string="Margin Top", default=60)
    date_margin_left = fields.Integer(string="Margin Left", default=792)

    source_margin_top = fields.Integer(string="Margin Top", default=60)
    source_margin_left = fields.Integer(string="Margin Left", default=12)

    recipient_margin_top = fields.Integer(string="Margin Top", default=37)
    recipient_margin_left = fields.Integer(string="Margin Left", default=60)

    amount_margin_top = fields.Integer(string="Margin Top", default=180)
    amount_margin_left = fields.Integer(string="Margin Left", default=800)

    text_amount_margin_top = fields.Integer(string="Margin Top", default=150)
    text_amount_margin_left = fields.Integer(string="Margin Left", default=20)

    signatory_margin_top = fields.Integer(string="Margin Top", default=100)
    signatory_margin_left = fields.Integer(string="Margin Left", default=20)

    def get_html_date(self, date):
        return """ 
            <div style="top:{}px;left:{}px;position:absolute;">
                {}
            </div>
            """.format(self.date_margin_top, self.date_margin_left, date)

    def get_html_source(self, source):
        return """ 
            <div style="top:{}px;left:{}px;position:absolute;">
                {}
            </div>
            """.format(self.source_margin_top, self.source_margin_left, source)

    def get_html_recipient(self, recipient):
        return """ 
            <div style="top:{}px;left:{}px;position:absolute;">
                {}
            </div>
            """.format(self.recipient_margin_top, self.recipient_margin_left, recipient)

    def get_html_amount(self, amount):
        return """ 
            <div style="top:{}px;left:{}px;position:absolute;">
                {}
            </div>
            """.format(self.amount_margin_top, self.amount_margin_left, amount)

    def get_html_text_amount(self, amount):
        text_amount = num2words(amount, lang="ar")
        return """ 
            <div style="top:{}px;left:{}px;position:absolute;">
                {}
            </div>
            """.format(self.text_amount_margin_top, self.text_amount_margin_left, text_amount)

    def get_html_signatory(self, signatory):
        return """ 
            <div style="top:{}px;left:{}px;position:absolute;">
                {}
            </div>
            """.format(self.signatory_margin_top, self.signatory_margin_left, signatory)

    def get_html_style(self):
        return """
            <style>
                div {
                      font-size: %spx;
                    }
            </style>
            """ % self.font_size
