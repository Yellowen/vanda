function WidgetArea (name, es) {
    Block.call(this, name, es);

    var el = this.element_id;
    var self = this;
    /*$(el).ready(function (){
	
    };*/

};

WidgetArea.prototype = new Block();
WidgetArea.prototype.constructor = WidgetArea;
WidgetArea.prototype.append_widget = function (widget) {
    document.tmp = this;
    async = this.async_ajax;
    if (widget.name in document.dashboard.widgets)
    {
	widget.name = widget.name + "_"
	widget.element_id = widget.element_id + "_"
    }

    document.dashboard.widgets[widget.name] = widget;
    $.ajax({url: widget.base_url,
	    method: "GET",
	    async: async,
	    success: function(data){
		block = document.tmp;
		delete document.tmp;
		block.widgets[widget.name] = widget;
		new_widget = $("#widget_data").html();
		$(new_widget).filter(".widgetbox").attr("id", "id_" + widget.name + "_wbox");
		console.log($(new_widget).filter(".widgetbar"));
		$(new_widget).filter(".widget").last().attr("id", "id_" + widget.name + "_wbar");
		console.log(new_widget);
		$(new_widget).filter(".widgetbox").html(data);
		$(block.es).append(new_widget);
		var width =  $(block.es).find("#id_" + widget.name + "_wbox").css("width");
		var p = $(block.es).find("#id_" + widget.name + "_wbox").css("padding-top");
		var w = $(block.es).find("#id_" + widget.name + "_wbar").width();
		console.log(w);

		$(block.es).find(".widget").css("width", aa + 58);
		$(block.es).find(".widget").attr("id", "id_" + widget.name + "_widget");
		
	    }
	   });
};
document.blocks["WidgetArea"] = WidgetArea;
