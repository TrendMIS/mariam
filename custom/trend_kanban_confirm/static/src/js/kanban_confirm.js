odoo.define('trend_kanban_confirm.kanban_confirm', function (require) {
"use strict";
var KanbanController = require('web.KanbanController');

KanbanController.include({
    _onAddRecordToColumn: function (ev) {
        var record = ev.data.record;
        var column = ev.target;
        if(column.modelName == "crm.lead" && (column.title == 'Lost' || column.title == 'Won')){
            if(!confirm(`Are you sure to move this lead to ${column.title}`)){
                location.reload();
                return
            }
        }
        this._super.apply(this, arguments);
    }
});
});
