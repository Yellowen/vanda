function SettingButton (n, e, u) {
    Widget.call(this, n, e, u);

    var el = this.element_id;
    var self = this;
    $(el).ready(function (){

	$(el).live({
	    mouseenter: function(){
		$(el + " img").attr("src", document.media_url + "image/settings-hover.png");
		
	    },
	    mouseleave: function(){
		$(el + " img").attr("src", document.media_url + "image/settings.png");
	    }});

	$(el).live("click", function(){

	    if ("is_open" in document.dashboard.blocks.config) {
		document.dashboard.blocks.config.hide();
		delete document.dashboard.blocks.config.is_open;
	    }
	    else {
		var a = document.dashboard.blocks.header.widgets;
		for (var widget in a){
		    if (! (a[widget].name == this.name)) {
			a[widget].close();
		    }
		}
		document.dashboard.blocks.config.show_url(self.base_url + "config/form/");
		document.dashboard.blocks.config.is_open = true;
	    }
	});
    });
};

SettingButton.prototype = new Widget();
SettingButton.prototype.constructor = SettingButton;
SettingButton.prototype.close = function(){
    if ("is_open" in document.dashboard.blocks.config) {
	document.dashboard.blocks.config.hide();
	delete document.dashboard.blocks.config.is_open;
    }
};
document.widgets["SettingButton"] = SettingButton;
