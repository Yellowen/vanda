function UltraBlog (n, e, u) {
    Widget.call(this, n, e, u);
    var el = this.element_id;
    var self = this;

}

UltraBlog.prototype = new Widget();
UltraBlog.prototype.constructor = UltraBlog;
UltraBlog.prototype.on_load = function(){
    $("#id_" + this.name + "_widget .tab-container").easytabs();
    var blog_config;
    var service = false;

    if ("ultra_blog" in localStorage) {
	blog_config = localStorage.getItem("ultra_blog");
	if (self.name in blog_config) {
	    service = blog_config[self.name].service | "http://www.yellowers.com:8000";
	}
    }
    else {
	blog_config = {};
	service = "http://www.yellowers.com:8000";
    }
    if (service.match(".*/$")){
	a = service.length - 1;
	service = service.substr(0, a);
    }
    console.log("ASD");
    console.log(service);
    $.getJSON(service + "/api/v1/blog/?",
	  {
	      authors__exact: document.current_user.id
	  },
	  function (data){
	      //for(var blog in data.objects) {
	      blog_config[self.name].blogs = data.objects
	      localStorage.setItem("ultra_blog", blog_config)
	      //}
	  });
};
document.widgets["UltraBlog"] = UltraBlog;
