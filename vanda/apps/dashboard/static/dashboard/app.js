define([
    'jquery',
    'underscore',
    'backbone',
    'router',
    'views/dashboard',
], function($, _, Backbone, Router, Dashboard){
    var initialize = function(){
	Router.initialize();
	// TODO: Retrieve the user loaded widgets and preferences.
	document.dashboard = new Dashboard();
    }

    return {
	initialize: initialize
    };
});
