require.config({
    shim: {
        'backbone': {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
	'relational': {
	    deps: ['backbone', ],
	}
    },
    paths: {
	jquery: 'lib/jquery/jquery',
	underscore: 'lib/underscore/underscore.min',
	backbone: 'lib/backbone/backbone',
	relational: 'lib/backbone/backbone-relational',
	bbloader: 'lib/backbone/bbloader',
    }
});

require([
    // Load our app module and pass it to our definition function
    'app',
], function(App){
    // The "app" dependency is passed in as "App"

    "use strict";
    App.initialize();
});
