function UltraBlog (n, e, u) {
    Widget.call(this, n, e, u);
    var el = this.element_id;
    var self = this;

}

UltraBlog.prototype = new Widget();
UltraBlog.prototype.constructor = UltraBlog;
UltraBlog.prototype.on_load = function(){
    $("#id_" + this.name + "_widget .tab-container").easytabs();
};
document.widgets["UltraBlog"] = UltraBlog;
