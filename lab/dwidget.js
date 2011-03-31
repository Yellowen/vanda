(function($) {

    var log = function(msg){
	var debug = window.debug || false
	if (debug == true)
	    console.log("[dwidget] >>> " + msg);
    };

// Resize ----------------------------------------------
   $.extend($.fn, {
        getCss: function(key) {
            var v = parseInt(this.css(key));
            if (isNaN(v))
                return false;
            return v;
        }
    });
    $.fn.resizable = function(opts) {
        var ps = $.extend({
            handler: null,
            min: { width: 0, height: 0 },
            max: { width: $(document).width(), height: $(document).height() },
            onResize: function() { },
            onStop: function() { }
        }, opts);
        var resize = {
            resize: function(e) {
                var resizeData = e.data.resizeData;

                var w = Math.min(Math.max(e.pageX - resizeData.offLeft + resizeData.width, resizeData.min.width), ps.max.width);
                var h = Math.min(Math.max(e.pageY - resizeData.offTop + resizeData.height, resizeData.min.height), ps.max.height);
                resizeData.target.css({
                    width: w,
                    height: h
                });
                resizeData.onResize(e);
            },
            stop: function(e) {
                e.data.resizeData.onStop(e);

                document.body.onselectstart = function() { return true; }
                e.data.resizeData.target.css('-moz-user-select', '');

                $().unbind('mousemove', resize.resize)
                    .unbind('mouseup', resize.stop);
            }
        }
        return this.each(function() {
            var me = this;
            var handler = null;
            if (typeof ps.handler == 'undefined' || ps.handler == null)
                handler = $(me);
            else
                handler = (typeof ps.handler == 'string' ? $(ps.handler, this) : ps.handle);
            handler.bind('mousedown', { e: me }, function(s) {
                var target = $(s.data.e);
                var resizeData = {
                    width: target.width() || target.getCss('width'),
                    height: target.height() || target.getCss('height'),
                    offLeft: s.pageX,
                    offTop: s.pageY,
                    onResize: ps.onResize,
                    onStop: ps.onStop,
                    target: target,
                    min: ps.min,
                    max: ps.max
                }

                document.body.onselectstart = function() { return false; }
                target.css('-moz-user-select', 'none');

                $().bind('mousemove', { resizeData: resizeData }, resize.resize)
                    .bind('mouseup', { resizeData: resizeData }, resize.stop);
            });
        });
    }

// Drag'n'Drop ---------------------------------------------
    $.extend($.fn, {
        getCss: function(key) {
            var v = parseInt(this.css(key));
            if (isNaN(v))
                return false;
            return v;
        }
    });
    $.fn.Drags = function(opts) {
        var ps = $.extend({
            zIndex: 20,
            opacity: .7,
            handler: null,
            onMove: function() { },
            onDrop: function() { }
        }, opts);
        var dragndrop = {
            drag: function(e) {
                var dragData = e.data.dragData;
                dragData.target.css({
                    left: dragData.left + e.pageX - dragData.offLeft,
                    top: dragData.top + e.pageY - dragData.offTop
                });
                dragData.handler.css({ cursor: 'move' });
                dragData.onMove(e);
            },
            drop: function(e) {
                var dragData = e.data.dragData;
                dragData.target.css(dragData.oldCss); //.css({ 'opacity': '' });
                dragData.handler.css('cursor', dragData.oldCss.cursor);
                dragData.onDrop(e);
                $().unbind('mousemove', dragndrop.drag)
                    .unbind('mouseup', dragndrop.drop);
            }
        }
        return this.each(function() {
            var me = this;
            var handler = null;
            if (typeof ps.handler == 'undefined' || ps.handler == null)
                handler = $(me);
            else
                handler = (typeof ps.handler == 'string' ? $(ps.handler, this) : ps.handle);
            handler.bind('mousedown', { e: me }, function(s) {
                var target = $(s.data.e);
                var oldCss = {};
                if (target.css('position') != 'absolute') {
                    try {
                        target.position(oldCss);
                    } catch (ex) { }
                    target.css('position', 'absolute');
                }
                oldCss.cursor = target.css('cursor') || 'default';
                oldCss.opacity = target.getCss('opacity') || 1;
                var dragData = {
                    left: oldCss.left || target.getCss('left') || 0,
                    top: oldCss.top || target.getCss('top') || 0,
                    width: target.width() || target.getCss('width'),
                    height: target.height() || target.getCss('height'),
                    offLeft: s.pageX,
                    offTop: s.pageY,
                    oldCss: oldCss,
                    onMove: ps.onMove,
                    onDrop: ps.onDrop,
                    handler: handler,
                    target: target
                }
                target.css('opacity', ps.opacity);
                $().bind('mousemove', { dragData: dragData }, dragndrop.drag)
                    .bind('mouseup', { dragData: dragData }, dragndrop.drop);
            });
        });
    }

// widget -----------------------------------------
    // plugin defination
    $.fn.dwidget = function(parameters) {
	
	var params = parameters || {};
	var defaults = {width: 100,
			height: 100,
			resizable: true,
			draggable: true
			};

	if (window.debug == true)
	    this.debug = true;
	else
	    this.debug = false;
	
	// Setup development environment -------
	if (this.debug){
	    $(this).css("background", "#444444");
	    $(this).css("color", "#eeeeee");
	}

	// --------------------------------------
	
	getparam = function(param){
	    return params[param] || defaults[param] || undefined;
	};

	// Setup widget --------------------------
	$(this).css("position", "absolute");
	$(this).css("width", getparam("width"));
	$(this).css("height", getparam("height"));
	

	// Set the widget draggable attribute

	if (getparam("draggable")){
	    $(this).Drags({
                onDrop:function(e){
                    $(this).html('dropped!');
                },
                zIndex:200,
                opacity:.9
            });
	}
	// Set the widget resizable attribute
	/*if (getparam("resizable")){
	    $(this).resizable({
                //handler: '.handler',
                min: { width: 300, height: 150 },
                max: { width: 500, height: 400 }
                /*onResize: function(e) {
                    state.html('target style: {width: ' +
			       e.data.resizeData.target.css('width') + ', height: ' +
                               e.data.resizeData.target.css('height') + '}');
                },
                onStop: function(e) {
                    $('#state').html('stopped');
                }
            });
	    this.create_child = function(params){};
	}*/
	
	$(this).html("Hello world " + this.debug);
	return this;

};  
})(jQuery); 