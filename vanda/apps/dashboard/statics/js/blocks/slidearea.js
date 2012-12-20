function SlideArea (name, es) {
    Block.call(this, name, es);
};

SlideArea.prototype = new Block();
SlideArea.prototype.constructor = SlideArea;

SlideArea.prototype.show = function (widget){
    this.async_ajax = false;
    this.element.slideDown('slow', "linear", this.load_widget(widget));
};
SlideArea.prototype.show_url = function (url){
    this.async_ajax = false;
    this.load_url(url);
    h = this.element.height();
    this.element.children().hide()
    this.element.height(h);
    var self = this;
    this.element.slideDown('normal', function(){
	self.element.children().fadeIn()
    });
};
SlideArea.prototype.hide = function (){
    var self = this;
    this.element.children().fadeOut("slow", function(){
	self.element.slideUp('noraml', "linear");
	self.element.html("");
    });
    
};

document.blocks["SlideArea"] = SlideArea;
