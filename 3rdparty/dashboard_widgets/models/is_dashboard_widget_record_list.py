from odoo import api, fields, models


class IsDashboardWidgetTableColumn(models.Model):
    _name = 'is.dashboard.widget.record_list.column'
    _description = 'Dashboard record list field'
    _order = 'sequence'

    sequence = fields.Integer()
    name = fields.Char(string="Label", required=True)
    field_id = fields.Many2one('ir.model.fields', string="Column")
    dashboard_id = fields.Many2one('is.dashboard.widget')
    column_class = fields.Char()
    format_string = fields.Char(string="Display Format", help="Python format string eg. '${:.2f}'")

    @api.onchange('field_id')
    def onchange_name(self):
        for rec in self:
            rec.name = rec.field_id.field_description or rec.field_id.field_description

    def get_value(self, record):
        value = record[self.field_id.name]
        if isinstance(value, models.Model) and len(value) > 1:
            return ', '.join(self._get_value(v) for v in value)
        else:
            return self._get_value(value)

    def _get_value(self, value):
        if hasattr(value, 'display_name'):
            value = value.display_name
        elif hasattr(value, 'name'):
            value = value.name
        if self.format_string:
            value = self.format_string.format(value)
        return value


class DashboardWidgetRecordList(models.Model):
    _inherit = 'is.dashboard.widget'

    display_mode = fields.Selection(selection_add=[
        ('record_list', 'Record List'),
    ])

    record_list_column_ids = fields.One2many(string="Columns", comodel_name='is.dashboard.widget.record_list.column', inverse_name='dashboard_id')

    def _get_record_display_name(self, record):
        # TODO: Use Odoo standard function to get this from rec_name, etc.
        if hasattr(record, 'display_name'):
            return record.display_name
        elif hasattr(record, 'name'):
            return record.name
        return "{}".format(record)

    def get_render_data(self):
        render_data = super(DashboardWidgetRecordList, self).get_render_data()

        if self.display_mode != 'record_list':
            return render_data

        if self.datasource == 'python':
            table_data = self.eval_data(self.query_1_table)
            if not table_data:
                return render_data
        else:
            if not self.query_1_config_model_id:
                render_data['error'] = "Please set a record type by editing this dashboard item"
                return render_data
            records = self.get_query_result(
                self.query_1_config_model_id,
                self.get_query_1_domain(),
                self.get_group_by_tuple(self.query_1_config_measure_field_id, self.query_1_config_measure_operator, date_only_aggregate=False),
                orderby="{} {}".format(self.chart_1_config_sort_field_id.name, "DESC" if self.chart_1_config_sort_descending else "ASC") if self.chart_1_config_sort_field_id else "",
                limit=self.query_1_config_result_limit or 100,
                sudo=self.query_1_sudo,
                return_record_set=True,
            )


        headers = [{
            'name': column.name,
        } for column in self.record_list_column_ids]

        render_data['table'] = {
            'record': self,
            'headers': headers,
            'rows': [[{
                'value': self.record_list_column_ids[icolumn].get_value(record),
                'display_value': self.record_list_column_ids[icolumn].get_value(record),
                'class': column.column_class or '',
                'action': {
                    'type': 'object',
                    'name': 'action_table_action',
                    'class': 'oe_kanban_action',
                    'context': {
                        'action_model': self.query_1_config_model_id.model,
                        'action_domain': [('id', 'in', records.ids)],
                        'action_name': self._get_record_display_name(record),
                        'open_form_view_res_id': record.id,
                    }
                },
            } for icolumn, column in enumerate(self.record_list_column_ids)] for record in records],
        }

        return render_data
