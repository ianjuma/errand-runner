var app = app || {};

/*
(function() {

	tagName: '',

	events: {
		'dblclick label': 'edit',
		'keypress .edit': 'updateOnEnter',
		'blur .edit': 'close'
	},

	render: function() {

	},

})();
*/

var TodoView = Backbone.View.extend({
	  tagName:  'li',
	  className: 'todos',
	  id: '',

	  // Cache the template function for a single item.
	  todoTpl: _.template( "An example template" ),

	  events: {
	    'dblclick label': 'edit',
	    'keypress .edit': 'updateOnEnter',
	    'blur .edit':   'close'
	  },

	  // Re-render the title of the todo item.
	  render: function() {
	    this.$el.html( this.todoTpl( this.model.toJSON() ) );
	    this.input = this.$('.edit');
	    return this;
	  },

	  edit: function() {
	    // executed when todo label is double clicked
	  },

	  close: function() {
	    // executed when todo loses focus
	  },

	  updateOnEnter: function( e ) {
	    // executed on each keypress when in todo edit mode,
	    // but we'll wait for enter to get in action
	  }
});

var viewUn = new TodoView();

console.log(viewUn.el);

// setElement + events and templating on views

var button1 = $('<button></button>');
var button2 = $('<button></button>');

var View = Backbone.View.extend({
	events: {
		click: function(e) {
			console.log(view.el === e.target);
		}
	}
});

var view = new View({el: button1});

view.setElement(button2);

button1.trigger('click');
button2.trigger('click');


var otherView = new Backbone.View;
otherView.setElement('<p><a><b>test</b></a></p>');
otherView.$('a b').html();