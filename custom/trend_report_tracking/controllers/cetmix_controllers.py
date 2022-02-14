from odoo import http, _
from odoo.addons.web.controllers.main import ReportController


class PrtReportController(ReportController):
    @http.route(['/report/<converter>/<reportname>', '/report/<converter>/<reportname>/<docids>', ], type='http',
                auth='user', website=True)
    def report_routes(self, reportname, docids=None, converter=None, **data):
        # report = request.env['ir.actions.report']._get_report_from_name(reportname)
        # model = report.model
        # res_id = docids
        # record = request.env[model].browse(int(res_id))
        # message = _('Print Report: %s') % report.name
        # record.message_post(body=message)
        return super().report_routes(reportname, docids, converter, **data)
