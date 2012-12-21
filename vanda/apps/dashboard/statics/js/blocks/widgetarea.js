function WidgetArea (name, es) {
    Block.call(this, name, es);

    var el = this.element_id;
    var self = this;
    $(el).ready(function (){
	$(".closebtn").live("click", function(){
	    var widgetname = $(this).parent().attr("widgetname");
	    $("#id_" + widgetname + "_widget").fadeOut(600, function(){$(this).remove()});
	    delete document.dashboard.widgets[widgetname];
	});
    });
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
		var new_widget = $("#widget_data").html();
		$("#tmp_widget").html(new_widget);
		new_widget = $("#tmp_widget");
		$(new_widget).find(".widgetbox").attr("id", "id_" + widget.name + "_wbox");
		$(new_widget).find(".widgetbox").attr("widgetname", widget.name);

		$(new_widget).find(".widgetbar").attr("id", "id_" + widget.name + "_wbar");
		$(new_widget).find(".widgetbar").attr("widgetname", widget.name);

		$(new_widget).find(".widget").attr("id", "id_" + widget.name + "_widget");
		$(new_widget).find(".widget").hide();
		$(new_widget).find(".widgetbox").html(data);
		var p = parseInt($(new_widget).find("#id_" + widget.name + "_wbox").css("padding-top"));
		var w = $(new_widget).find("#id_" + widget.name + "_wbar").width();

		$(block.es).append(new_widget.html());
		$(block.es).find("#id_" + widget.name + "_widget").fadeIn(600);
		var width =  parseInt($(block.es).find("#id_" + widget.name + "_wbox").width());
		var fwidth = width + p * 2 + w;

		$(block.es).find("#id_"+ widget.name + "_widget").css("width", fwidth);

		$("#tmp_widget").html("");
	    }
	   });
};
document.blocks["WidgetArea"] = WidgetArea;
