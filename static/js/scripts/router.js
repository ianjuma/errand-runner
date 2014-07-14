App = App || {}; // app namespace

App.router = Backbone.Router.extend({
	  routes: {
		    "api/v0.0.1/member/:id": "getMem",
        "*actions": "defaultRoute", // /#anything-here
        "help": "help",    // #help
    	  "search/:query": "search",  // #search/query
    },
    help: function() {
    	
  	},
  	search: function(query, page) {
    	
  	}
});

var AppRouter = new app.router;


AppRouter.on('route:defaultRoute', function(actions) {
	alert(actions);
});


AppRouter.on('route:getMem', function(actions) {
	alert(actions);
});

// Start Backbone history a necessary step for bookmarkable URL's
Backbone.history.start();