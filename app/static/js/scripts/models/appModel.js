// AppModel

var Todo = Backbone.Model.extend({
	initialize: function() {
		console.log('This model has been initialized');

		this.on("change", function(){
			console.log("Attributes in this Model have changed");
		});
	},

	defaults: {
		title: '',
		completed: ''
	},
});

var todoModel = new Todo();

var todoModel2 = new Todo({
	title: '',
	completed: 'false',
});

todoModel2.set({title: "Java class", completed: "true"});

console.log(JSON.stringify(todoModel2));

var someOtherTodo = new Todo();

console.log(someOtherTodo.toJSON());

todoModel2.set("title", "I dont know what this is");
todoModel2.set({title: "I know what this is"});

todoModel2.on("change:title", function() { console.log("Model has changed"); });
todoModel2.set({title: "Aha!"});
todoModel2.set({title: "No!"});


// silence on change of an attribute
todoModel2.set({title: "Jo!"}, {silent: true});


console.log(todoModel2.hasChanged("title")); // --event listener
todoModel2.hasChanged(null); //check if any attributes changed

console.log("it should not log a change");

todoModel2.set(
	{ title: "Ian", completed: true },
	{ silent: true }
);

// log change on a specific attribute

var Beatles = Backbone.Model.extend({
	defaults: {
		name: '',
		age: 10,
		dob: ''
	},
	
	validate: function(attributes) {
		if (!attributes.name) {
			return "Set name in Model";
		}

		if (!attributes.age) {
			return "Set age in Model";
		}

		if (!attributes.dob) {
			return "Set dob in Model"
		}
	},

	initialize: function(){
		this.on('change:name', function(){
			console.log("The name in this attribute changed");
		});
	},

	setName: function(newName) {
		this.set({name: newName});
	}
});

var theBeatles = [
	{'name': 'John', 'age': 12, 'dob': ''},
	{'name': 'Stooge', 'age': 23, 'dob': ''},
	{'name': 'Alex', 'age': 45, 'dob': ''},
	{'name': 'Cisse', 'age': 26, 'dob': ''}
];

var BeatlePerson = new Beatles();

BeatlePerson.validate = function(attrs) {
	if (!attrs.name) {
		console.log("name is needed");
		return "Name is needed";
	}

	if (!attrs.age) {
		console.log("age is needed");
		return "Age is Needed";
	}
}

console.log(BeatlePerson.get('name'));


_.forEach(theBeatles, function(member) {
	BeatlePerson.set(member);
});

BeatlePerson.set(theBeatles[0]);
console.log(BeatlePerson.get('name'));

BeatlePerson.setName("Ian");
console.log(BeatlePerson.toJSON());

BeatlePerson.set({name: "John"}, {validate: true});
BeatlePerson.unset("name", {validate: true});