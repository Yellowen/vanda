define([
    'underscore',
    'backbone',
    'relational',
], function(_, Backbone) {

    Backbone.api_url = "/api/v1";

    Backbone.TModel = Backbone.Model.extend({
	url: function() {
	    var temp_url = this.base_url;
	    if (this.isNew()) {
		return Backbone.api_url + (temp_url.charAt(temp_url.length - 1) == '/' ? temp_url : temp_url+'/');
	    }
	    return Backbone.api_url + (temp_url.charAt(temp_url.length - 1) == '/' ? temp_url : temp_url+'/') + encodeURIComponent(this.get('id')) + '/' ;
	},
	fields: function(){}
    });

    // Our Backbone Model implementation with relation support.
    Backbone.RTModel = Backbone.RelationalModel.extend({
	url: function() {
	    var temp_url = this.base_url;
	    if (this.isNew()) {
		return Backbone.api_url + (temp_url.charAt(temp_url.length - 1) == '/' ? temp_url : temp_url+'/');
	    }
	    return Backbone.api_url + (temp_url.charAt(temp_url.length - 1) == '/' ? temp_url : temp_url+'/') + encodeURIComponent(this.get('id')) + '/' ;
	},
	fields: function(){}
    });

    Backbone.TCollection = Backbone.Collection.extend({
	parse: function(response) {
            this.recent_meta = response.meta || {};
            return response.objects || response;
	},
	url: function() {
	    var temp_url = this.base_url;
	    return Backbone.api_url + (temp_url.charAt(temp_url.length - 1) == '/' ? temp_url : temp_url+'/');
	}

    });

    Backbone.View = Backbone.View.extend ({
	get_form_value: function(key, prefix_){
	    // Return a form value using a map of "key": "inputid"
	    if (key === undefined) throw "Key argumant should not be undefined";
	    if (key in this.form_dict) {
		var prefix = prefix_ || "";
		var id = this.form_dict[key];
		return $("#" + prefix + id).val();
	    }
	    return undefined
	},
	set_form_value: function(key, value_, prefix_){
	    // Set a form value using a map of "key": "inputid"
	    if (key === undefined) throw "Key argumant should not be undefined";
	    if (key in this.form_dict) {
		var value = value_ || "";
		var prefix = prefix_ || "";
		var id = this.form_dict[key];
		$("#" + prefix + id).val(value);
		return true;
	    }
	    return false;
	},
	update_model_from_form: function (model, prefix_, commit_, options){
	    if (model === undefined) throw "model should be specified";
	    var prefix = prefix_ || "";
	    var commit = true;
	    if (commit_ !== undefined) {
		commit = commit_;
	    }
	    var that = this;
	    _.each(model.fields(), function (key) {
		var value = that.get_form_value(key, prefix);

		if (! (value === undefined)) {
		    model.set(key, value);
		}
	    });
	    if (commit == true) {
		model.save(options);

	    }
	    return model;
	},
    });
    return Backbone;
});
