App = App || {};

App.MemberView = Backbone.View.extend({
	
	el: 'div',
	tagName:  'div',
	className: 'member',
	id: 'memberView',

	events: {
	    'click label': 'edit',
	    'click .save': 'updateOnEnter',
	    'click .refresh':   'close',
	    'click .diag-engine': 'diagEngine',
	    'click .reset-All': 'resetAll',
	},

	template: Handlebars.compile($("#memberView").html()),

	initialize: function() {
		this.model = App.User;
		this.render();
		_.bindAll(this, 'render');
		this.model.bind('change', this.render);
		this.model.bind('reset', this.render);
        this.model.view = this;
	},

	render: function() {
		this.$el.html( this.template(this.model.toJSON() ));
		// var dict = this.model.toJSON();
		// var html = this.template(dict);

		// $(this.el).append(html);
		return this;
	},

	edit: function() {

	},

	close: function() {

	},

	updateOnEnter: function() {

	},

});