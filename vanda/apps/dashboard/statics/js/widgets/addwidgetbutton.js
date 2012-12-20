function AddWidgetButton (n, e, u) {
    Widget.call(this, n, e, u);

    var el = this.element_id;
    var self = this;
    $(el).ready(function (){

	$(el).live({
	    mouseenter: function(){
		$(el + " img").attr("src", document.media_url + "image/add-hover.png");
		
	    },
	    mouseleave: function(){
		$(el + " img").attr("src", document.media_url + "image/add.png");
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
		document.dashboard.blocks.config.show_url(self.base_url + "list/");
		document.dashboard.blocks.config.is_open = true;
	    }
	});
	console.log(self.name);
	document.dashboard.blocks.config.element.find("#id_" + self.name + "_button").live("click", function(){
	    var widget_name = $(document.dashboard.blocks.config.es).find("#id_" + self.name + "_select").val();
	    if (widget_name === undefined) { alert("WIW");}
	    document.dashboard.blocks.body.append_widget(document.dashboard.widgets[widget_name]);
	});
    });
};

AddWidgetButton.prototype = new Widget();
AddWidgetButton.prototype.constructor = AddWidgetButton;
AddWidgetButton.prototype.close = function(){
    if ("is_open" in document.dashboard.blocks.config) {
	document.dashboard.blocks.config.hide();
	delete document.dashboard.blocks.config.is_open;
    }
};
document.widgets["AddWidgetButton"] = AddWidgetButton;
