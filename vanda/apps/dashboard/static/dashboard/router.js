define([
    'jquery',
    'underscore',
    'bbloader',
], function($, _, Backbone){
    var AppRouter = Backbone.Router.extend({
	routes: {
	    'menus': 'menuslist',
	    'store': 'storelist',
	    'employees': 'employeeslist',
	    'group': 'group',
	    '*actions': 'default_action'
	}
    });

    var initialize = function(){
	var router = new AppRouter();

	router.on('route:storelist', function(){
	    require(['views/store/list'], function(View){
		var view = new View();
		view.render();
	    });
	});

	router.on('route:employeeslist', function(){
	    require(['views/employee/list'], function(View){
		var view = new View();
		view.render();
	    });
	});

	router.on('route:group', function(){
	    require(['views/group/list'], function(View){
		var view = new View();
		view.render();
	    });
	});

	router.on('route:menuslist', function(){
	    require(['views/menu/list'], function(View){
		var view = new View();
		view.render();
	    });
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
