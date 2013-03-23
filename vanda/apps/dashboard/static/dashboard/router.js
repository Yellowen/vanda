define([
    'jquery',
    'underscore',
    'bbloader',
], function($, _, Backbone){
    var AppRouter = Backbone.Router.extend({
	routes: {
	    'widgets': 'widgets',
	    '*actions': 'default_action'
	}
    });

    var initialize = function(){
	var router = new AppRouter();

	router.on('route:widgets', function(){
	    console.log("shit");
	    /*require(['views/store/list'], function(View){
		var view = new View();
		view.render();
	    });*/
	});

	router.on('default_action', function(actions){
	    console.log('No route:' +  actions);

	});

	Backbone.history.start();
    };

    return {
	initialize: initialize
    };
});
