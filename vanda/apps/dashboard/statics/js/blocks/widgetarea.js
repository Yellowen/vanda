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
		data_width = $(data).width();
		data_height = $(data).height();
		console.log(data_width);
		console.log(data_height);
		new_widget = $("#widget_data").html();

		width = data_width + $(new_widget).css("padding") * 2;
		console.log(width);
		$(new_widget).filter(".widgetbox").attr("id", "id_" + widget.name + "_wbox");
		$(new_widget).filter(".widgetbar").attr("id", "id_" + widget.name + "_wbar");
		$(new_widget).filter(".widget").attr("id", "id_" + widget.name + "_widget");
		$(new_widget).filter(".widgetbox").html(data);
		$(block.es).append(new_widget);
		
	    }
	   });
};
document.blocks["WidgetArea"] = WidgetArea;
