function UltraBlog (n, e, u) {
    Widget.call(this, n, e, u);
    var el = this.element_id;
    var self = this;

}

UltraBlog.prototype = new Widget();
UltraBlog.prototype.constructor = UltraBlog;
UltraBlog.prototype.constructor = UltraBlog;
UltraBlog.prototype.refresh_data = function(serviceurl){
    var service;
    var blog_config = {};
    var self = this;
    if (serviceurl === undefined){
 	service = "http://www.yellowers.com:8000";
	if ("ultra_blog" in localStorage) {
	    blog_config = JSON.parse(localStorage.getItem("ultra_blog"));
	    if (!(blog_config[self.name] === undefined)) {
		service = blog_config[self.name].service | "http://www.yellowers.com:8000";
	    }
	}
    }
    else {
	service = serviceurl;
    }
    if (service.match(".*/$")){
	a = service.length - 1;
	service = service.substr(0, a);
    }
    $.getJSON(service + "/api/v1/blog/?",
	  {
	      authors__exact: document.current_user.id
	  },
	  function (data){
	      if (!(blog_config[self.name] === undefined)){
		  console.log("Asd");
		  console.dir(data.objects);
		  blog_config[self.name].blogs = data.objects
		  blog_config[self.name].service = service
	      }
	      else {
		  blog_config = {blogs: data.objects,
				 service:service}
	      }
	      localStorage.setItem("ultra_blog", JSON.stringify(blog_config));
	  });

};
UltraBlog.prototype.on_load = function(){
    $("#id_" + this.name + "_widget .tab-container").easytabs();
    this.refresh_data();
    var self = this;
    $("#id_" + this.name + "_widget #settings-button").live("click", function(){
	var service = $("#id_" + self.name + "_widget #service-url").val();
	self.refresh_data(service);
	
    });
};
document.widgets["UltraBlog"] = UltraBlog;
