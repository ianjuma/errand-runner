// app namespace - use BC as a namespace -> var Bc = Bc || {};

App = App || {};

App.User = Backbone.Model.extend({

	urlRoot: "/api/v0.0.1/member/",

	initialize: function() {
		console.log('BetaModel has been initialized');
		url = '/api/v0.0.1/member/';

		this.on("change", function() {
			console.log("Attributes in this Model have changed");
		});
	},
	
	defaults: {
		fname: '',
		lname: '',
		location: '',
		blood_group: '',
		allergies: 'None',
		blood_rhesus: '',
		last_seen: '',
		patient_hist: '',
		sym_description: ''
	},

	setFname: function(newName) {
		this.set({fname: newName});
	},

	setLname: function(newName) {
		this.set({lname: newName});
	},

	validate: function(attrs) {
		if(attrs.fname === undefined) {
        	return "Name not set";
    	}
    	if (attrs.lname === undefined) {
    		return "lname not set";
    	}
    	if (attrs.location === undefined || attrs.allergies === undefined) {
    		return "location or allergies not set";
    	}
    	if (attrs.patient_hist === undefined) {
    		return "patient_hist not set";
    	}
    	if (attrs.blood_r === undefined || attrs.blood_g === undefined) {
    		return "Blood group or rhesus factor not set not set";
    	}
	},

	// change other attributes directly
});


/*
member.on("reset", function() {
    console.log(stores.toJSON());
});

member.fetch();
*/