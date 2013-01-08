$(function () {
    document.media_url = "{{ MEDIA_URL }}";
    document.current_user = {id: {{ request.user.id }},
			     username: "{{ request.user.username }}"
			    };
    document.dashboard = new Dashboard();
    var init_data = JSON.parse('{% autoescape off %}{{ blocks }}{% endautoescape %}');
    document.tmp = init_data;
    for (var key in init_data)
    {
	if (init_data[key].type in document.blocks) {
	    document.dashboard.add_block(new document.blocks[init_data[key].type](key, "#" + init_data[key].id));
	}
	else { throw "No block class found for " + key; }
    }
    var init_data = JSON.parse('{% autoescape off %}{{ widgets }}{% endautoescape %}');
    for (var key in init_data)
    {
	if (init_data[key].type in document.widgets) {
	    var w = new document.widgets[init_data[key].type](key, "#" + init_data[key].id, "{% url dashboard-index %}widgets/" + key + "/");
	    document.dashboard.add_widget(w);
	    if ("block" in init_data[key]) {
		document.dashboard.blocks[init_data[key].block].register(w);
	    }
	}
	else { throw "No widget class found for " + key; }

    }

});
