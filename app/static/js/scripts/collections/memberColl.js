App = App || {};

App.memberColl = Backbone.Collection.extend({
	model: App.User,
	url:'/api/v0.0.1/member/',
});