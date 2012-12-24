function Dashboard (){
    this.blocks = {}
    this.widgets = {}
};

Dashboard.prototype.add_block = function (block){
    if (!(block.name in this.blocks))
    {
	this.blocks[block.name] = block;
    }
};
Dashboard.prototype.get_blocks = function (){
    return this.blocks;
};
Dashboard.prototype.add_widget = function (widget){
    if (! (widget.name in this.widgets))
    {
	this.widgets[widget.name] = widget;
    }
};

function Block (name, element_selector){
    this.element = $(element_selector);
    this.es = element_selector;
    this.name = name;
    this.async_ajax = true;
    this.widgets = {};
    this.current_widgets = {};
};
Block.prototype.register = function (widget){
    if (!(widget.name in this.widgets))
    {
	this.widgets[widget.name] = widget;
    }
};

Block.prototype.show = function (){};
Block.prototype.hide = function (){};
Block.prototype.add_widget = function (){};
Block.prototype.load_url = function (url){
    async = this.async_ajax;
    document.tmp = this;
    $.ajax({url: url,
	    method: "GET",
	    async: async,
	    success: function(data){
		block = document.tmp;
		delete document.tmp;
		$(block.es).html(data);
	    }
	   });
};
Block.prototype.load_widget = function (widget){
    document.tmp = this;
    async = this.async_ajax;
    if (widget.name in this.current_widgets)
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
		$(block.es).html(data);
		widget.on_load();
	    }
	   });
};
Block.prototype.append_widget = function (widget){
    document.tmp = this;
    async = this.async_ajax;

    if (widget.name in this.current_widgets)
    {
	widget.name = widget.name + "_";
	widget.element_id = widget.element_id + "_";
    }
    document.dashboard.widgets[widget.name] = widget;
    this.current_widgets[widget.name] = widget;
    $.ajax({url: widget.base_url,
	    method: "GET",
	    async: async,
	    success: function(data){
		block = document.tmp;
		delete document.tmp;
		$(block.es).append(data);
		widget.on_load();
	    }
	   });
};

function Widget (name, element, base_url){
    this.element_id = element;
    this.base_url = base_url;
    this.name = name;
    
};

Widget.prototype.show = function (){};
Widget.prototype.hide = function (){};

document.blocks = {};
document.widgets = {};
