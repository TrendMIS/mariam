odoo.define('trend_kanban_lost.kanban_lost', function (require) {
    "use strict";
    var KanbanController = require('web.KanbanController');

    KanbanController.include({
        _onAddRecordToColumn: function (ev) {
            var record = ev.data.record;
            var column = ev.target;
            this._super.apply(this, arguments);
            if(column.title == 'Lost' && column.modelName == "crm.lead"){
                this.do_action({
                    type:'ir.actions.act_window',
                    res_model: "crm.lead.lost",
                    target: 'new',
                    views: [[false, 'form']],
                    context: {
                        'active_ids': [record.id],
                        'active_id': record.id,
                        'default_lead_id': record.id
                    }
                });
            }
        }
    });
});
