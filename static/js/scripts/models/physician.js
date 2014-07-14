App = App || {}; // app namespace

App.Physician = Backbone.Model.extend({

	//url: /api/v0.0.1/getPhy/_id || /api/v0.0.1/getPhy/fname

	urlRoot: "/api/v0.0.1/physician/",

	initialize: function() {
		console.log('BetaModel has been initialized');
		// url = '/api/v0.0.1/physician/';

		this.on("change", function() {
			console.log("Attributes in this Model have changed");
			console.log(this.toJSON());
		});
	},

	// json res
	defaults: {
		fname: '',
		lname: '',
		location: '',
		specialty: '',
		hospital: '',
		hist_about: '',
	},

	setFname: function(newName) {
		this.set({fname: newName});
	},

	setLname: function(newName) {
		this.set({lname: newName});
	},

	validate: function(attrs) {
		if(attributes.fname === undefined) {
        	return "Name not set";
    	}
    	if (attrs.lname === undefined) {
    		return "lname not set";
    	}
    	if (attrs.location === undefined || attrs.hospital === undefined) {
    		return "location or hospital not set";
    	}
    	if (attrs.hist_about === undefined) {
    		return "hist_about not set";
    	}
    	if (attrs.specialty === undefined) {
    		return "specialty not set";
    	}
	},

	setInterval(function() {
  		this.fetch();
	}, 10000);

	// change other attributes directly - change with one JSON object
});