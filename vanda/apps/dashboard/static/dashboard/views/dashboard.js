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
    'views/drawer',
    'views/notifier',
], function($, _, Backbone, Drawer, Notifier) {

    var DashboardView = Backbone.View.extend({
	initialize: function(){
	    this.drawer = new Drawer();
	    this.notification = new Notifier({'el': $("#notification-area")});
	    this.notification.hide();
	},

	el: $("#content"),

	events: {
	    "click .drawer-handle": "toggle_drawer",
	},

	render: function() {
	    // TODO: Load the defaults
	},

	toggle_drawer: function() {
	    this.notification.fadeIn(300);
	    this.drawer.toggle_drawer();
	    this.notification.fadeOut(300);
	},

    });

    return DashboardView;

});
