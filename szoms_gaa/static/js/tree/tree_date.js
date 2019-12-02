odoo.define("itsm.gaa_tree_date", function(require) {
	"use strict";

	var AbstractField = require("web.AbstractField");
	var field_registry = require("web.field_registry");

	var gaa_tree_date = AbstractField.extend({
		init: function() {
			this._super.apply(this, arguments);
		},
		_render: function() {
			var text =this.value
			var time = new Date(text*1000);
			var commonTime = time.toLocaleString();
			this.$el.html(commonTime);
		}
	});

	field_registry.add("gaa_tree_date", gaa_tree_date);
	return gaa_tree_date;
});
