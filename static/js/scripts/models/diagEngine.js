// var App = function() {}

App = App || {};

App.User = Backbone.Model.extend({

	urlRoot: "/api/v0.0.1/diagnosticEngine/",

	initialize: function() {
		console.log('diag_engine model has been initialized');

		this.on("change", function() {
			console.log("Attributes in this Model have changed");
		});
	},

	defaults: {
		dob: '',
		sex: '',
		pregnant: '',
		region: '',
		queryText: '',
	},

});