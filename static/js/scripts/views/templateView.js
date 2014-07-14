(function() {

	var ListView = Backbone.View.extend({

		el: 'div',
		className: 'contact',
		id: 'template-contact',

		events: {}, // empty events hash

		template: _.template($("#template-contact").html()),

		render: function() {

			var dict = this.model.toJSON();
			var html = this.template(dict);

			$(this.el).append(html);
			return this;
		}

	});

})();