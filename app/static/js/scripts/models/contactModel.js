(function() {
	var App = function() {}
	App = App;
	App = App || {};

	App.Todo = Backbone.Model.extend({

		urlRoot: '/api/betaMember/',

		initialize: function() {
			console.log('This model has been initialized');

			url = '/api/betaMember/';

			this.on("change", function() {
				console.log("Attributes in this Model have changed");
			});
		},

		/*
		setInterval: function() { setInterval(function() {
  				this.fetch();
			}, 10000);
		},
		*/

		defaults: {
			name: '',
			email: ''
		},

	});

	var contactModel = new App.Todo({
		name: "Ian",
		email: "wjuma@students.usiu.ac.ke"
	});


	var ContactCollection = Backbone.Collection.extend({
		model: App.Todo,
		url: '/api/betaMember/'
	});

	var coll = new ContactCollection();

	coll.add(contactModel);
	// coll.save(); // urlRoot - create

})();