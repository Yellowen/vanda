function UserButton (n, e, u) {
    Widget.call(this, n, e, u);
    var el = this.element_id;
    var self = this;
    $(el).ready(function (){

	$(el).live("click", function(){
	    for (var widget in document.dashboard.blocks.header.widgets){
		if (! (document.dashboard.blocks.header.widgets[widget].name == this.name)) {
		    document.dashboard.blocks.header.widgets[widget].close();
		}
	    }
	    var menu = $(".submenu[belongs_to='" + $(this).attr("id") + "']");
	    $(".submenu").not(menu).hide();
	    menu.fadeToggle("slow");
	});
    });
}

UserButton.prototype = new Widget();
UserButton.prototype.constructor = UserButton;
UserButton.prototype.close = function(){
    var menu = $(".submenu[belongs_to='" + $(this).attr("id") + "']");
    menu.hide();
};

document.widgets["UserButton"] = UserButton;

