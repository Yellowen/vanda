(function($) {
    // plugin defination
    $.fn.dwidget = function(parameters) {
	
	var self = this;

	var params = parameters || {};
	var defaults = {width: 100,
			 height: 100
			};

	if (window.debug == true)
	    self.debug = true;
	else
	    self.debug = false;

	self.log = function(msg){
	    if (self.debug == true)
		console.log("[dwidget] >>> " + msg);
	};
	
	// Setup development environment -------
	if (self.debug){
	    $(self).css("background", "#444444");
	    $(self).css("color", "#eeeeee");
	}

	// --------------------------------------
	
	getparam = function(param){
	    return params[param] || defaults[param] || undefined;
	};

	// Setup widget --------------------------
	self.log(getparam("width"));
	$(self).css("position", "absolute");
	$(self).css("width", getparam("width"));
	$(self).css("height", getparam("height"));
	
	self.create_child = function(params){};


	$(self).html("Hello world " + self.debug);
	return self;

};  
})(jQuery); 