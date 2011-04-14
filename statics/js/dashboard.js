/* dashboard.css
Copyright (C) 2011 Some Hackers In Town street computing group

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.
*/
function init_drawer(div, handler, max_size, min_size, property){
    div.css(property, min_size);
    handler.click(function(){
	var size = div.css(property);
	if (size == min_size){
	    var obj = {};
	    obj[property] = max_size;
	    div.animate(obj, 'slow');
	}
	else
	{
	    var obj = {};
	    obj[property] = min_size;
	    div.animate(obj, 'slow');
	}
    });
    return div;
};
$(function(){
    var ldrawer = init_drawer($("#ldrawer"), $("#lhandler"), "30%", "3px", "width")

});