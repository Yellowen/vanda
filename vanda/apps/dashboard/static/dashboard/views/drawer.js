/* -----------------------------------------------------------------------------
*    Vanda dashbord - Dashboard application of Vanda platform
*    Copyright (C) 2012-2013  Sameer Rahmani <lxsameer@gnu.org>
*
*    This program is free software; you can redistribute it and/or modify
*    it under the terms of the GNU General Public License as published by
*    the Free Software Foundation; either version 2 of the License, or
*    (at your option) any later version.
*
*    This program is distributed in the hope that it will be useful,
*    but WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*    GNU General Public License for more details.
*
*    You should have received a copy of the GNU General Public License along
*    with this program; if not, write to the Free Software Foundation, Inc.,
*    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
* ----------------------------------------------------------------------------- */
define([
    'jquery',
    'underscore',
    'bbloader',
], function($, _, Backbone) {

    var DrawerView = Backbone.View.extend({
	initialize: function(){
	    this.el = $("#drawer");
	    this.el.hide();
	},

	render: function() {
	},

	toggle_drawer: function() {
	    if (this.el.hasClass("opened")) {
		this.close_drawser();
	    }
	    else {
		this.open_drawser();
	    }
	},

	open_drawser: function(){
	    this.el.slideDown();
	    this.el.addClass("opened");
	},
	close_drawser: function(){
	    this.el.slideUp();
	    this.el.removeClass("opened");
	},
	show: function(){
	    this.el.show();
	},

    });

    return DrawerView;
});
