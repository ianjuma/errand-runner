var App = function() {}
App = App;

App.BetaView = Backbone.View.extend({

	initialize: function() {
		this.render();
	},

	tagName:  'div',
	className: 'beta',

	events: {
	    'dblclick label': 'edit',
	    'keypress .edit': 'updateOnEnter',
	    'blur .edit':   'close'
	},

	// Cache the template function for a single item.
	betaTpl: _.template( "An example template" ),

	render: function() {
	    this.$el.html( this.betaTpl( this.model.toJSON() ) );
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