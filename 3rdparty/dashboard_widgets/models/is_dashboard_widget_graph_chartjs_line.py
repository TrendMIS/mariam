from odoo import api, fields, models

from collections import OrderedDict
from odoo.exceptions import UserError


class DashboardWidgetGraph(models.Model):
    _inherit = 'is.dashboard.widget'

    def get_dataset_for_goal_1(self, dates, labels=None):
        if dates:
            return {
                'label': self.chart_1_goal_config_title,
                'data': [self.get_1_goal_for_date(date, False, current_goal_value_only=True) if date else 0 for date in dates],
                'domains': False,
                'date_start': False,
                'action_id': False,
            }
        elif labels:
            return {
                'label': self.chart_1_goal_config_title,
                'data': [self.goal_count for label in labels],
                'domains': False,
                'date_start': False,
                'action_id': False,
            }

    def _merge_datasets(self, data, ds):
        labels = data['data']['labels']
        new_labels = ds['labels']
        if labels != new_labels:
            self._add_render_dashboard_markup_error('_merge_datasets', "Data series labels must match to allow combining into a single chart")
        data['data']['datasets'] += ds['datasets']

    def update_dashboard_data_ds(self, data, datasets, color, area, title):
        super(DashboardWidgetGraph, self).update_dashboard_data_ds(data, datasets, color, area, title)
        if datasets and self.graph_type == 'line':
            for ds in datasets:
                if 'fill' not in ds:
                    ds['fill'] = area
                if color:
                    ds['pointColor'] = color
                    ds['pointBorderColor'] = color
                    ds['pointBackgroundColor'] = color
                    ds['borderColor'] = color
                    ds['backgroundColor'] = color

    def get_dashboard_data_add_ds(self, chart_datasets, data1, data2):
        if self.graph_type == 'line' and data1:
            if self.query_1_config_enable_goal and (data1['dates'] or self.goal_count):
                ds = self.get_dataset_for_goal_1(data1['dates'], data1['labels'])

                ds['fill'] = self.chart_1_goal_config_area

                if self.chart_1_goal_config_color:
                    ds['pointColor'] = self.chart_1_goal_config_color
                    ds['pointBorderColor'] = self.chart_1_goal_config_color
                    ds['pointBackgroundColor'] = self.chart_1_goal_config_color
                    ds['borderColor'] = self.chart_1_goal_config_color
                    ds['backgroundColor'] = self.chart_1_goal_config_color

                chart_datasets.append(ds)
