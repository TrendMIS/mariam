odoo.define('trend_pin_location.location', function (require) {
"use strict";

var framework = require('web.framework');
var FormController = require('web.FormController');

FormController.include({
	_onButtonClicked: function (ev) {
	    if(ev.data.attrs.name === "get_location"){
            var self = this;
            var record = self.model.get(self.handle, {raw: true})
            self.$('#get-location').attr("disabled", "disabled");
            navigator.geolocation.getCurrentPosition(function(position){
                framework.blockUI();
                var vals = {"lat": String(position.coords.latitude), "lng": String(position.coords.longitude)};
                self._rpc({
                    model: 'crm.lead',
                    method: 'write',
                    args: [[record.data.id], vals],
                }).then(function(result) {
                    framework.unblockUI();
                    window.location.reload();
                });
            });
        } else {
            return this._super(ev);
        }
	},
});

});