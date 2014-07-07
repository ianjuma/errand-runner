user.set({fname: 'Ian',
		lname: 'Juma',email: "ian.j",
		location: 'Nairobi',
		blood_g: 'O',
		allergies: 'None',
		blood_r: '-', dob: "08121992",
		last_seen: '08102013',
		patient_hist: 'None',
		sym_description: 'Tired'})


		User = Backbone.Model.extend({

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
		blood_g: '',
		allergies: '',
		blood_r: '',
		last_seen: '',
		patient_hist: '',
		sym_description: ''
	},

	setFname: function(newName) {
		this.set({fname: newName});
	},

	setLname: function(newName) {
		this.set({lname: newName});
	}, });
