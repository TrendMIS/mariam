import logging
import re

import requests

from odoo import models, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
ENDPOINT = "https://smsvas.vlserv.com/KannelSending/service.asmx/SendSMS"
VL_TO_SMS_STATE = {
    '0': 'success',
    '-5': 'insufficient_credit'
}


class SmsApi(models.AbstractModel):
    _inherit = 'sms.api'
    _description = 'SMS victorylink override'

    @api.model
    def _contact_iap(self, _, params):
        messages = params.get("messages")
        if messages:
            return self._send_messages(messages)
        return self._send_single_message(params['message'], params['numbers'])

    def get_param(self, param):
        config_param = f"sms.victorylink.{param}"
        value = self.env['ir.config_parameter'].sudo().get_param(config_param)
        if not value:
            raise UserError(_(f"Missing config {config_param}, please add it to configuration parameters"))
        return value

    def _send_messages(self, messages):
        results = []
        for message in messages:
            receiver = message['number']
            response_code = self._send_single_message(message['content'], receiver)
            results.append({
                'res_id': message['res_id'],
                'state': VL_TO_SMS_STATE.get(response_code, 'server_error')
            })
        return results

    def _send_single_message(self, content, numbers):
        username = self.get_param("username")
        password = self.get_param("password")
        sender = self.get_param("sender")
        sms_lang = "E" if [True for c in 'aeiouymn' if c in content] else "A"
        params = {
            'smsText': content,
            'SMSLang': sms_lang,
            'SMSSender': sender,
            'SMSReceiver': numbers
        }
        _logger.info(f"Sending Message with following params {params}")
        params.update({'UserName': username, 'password': password})
        response = requests.get(ENDPOINT, params=params)
        regex = re.compile(r'<int.*?>(.*?)</int>')
        response_code = regex.search(response.text)[1]
        if response_code != '0':
            _logger.error(f"Failed to send message with victorylink status code {response_code}")
        return str(response_code)
