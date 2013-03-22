/* -----------------------------------------------------------------------------
   YaTabs - Yet Another jquery tabs plugin
   Copyright (C) 2012-2013 Sameer Rahmani <lxsameer@gnu.org>

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License along
   with this program; if not, write to the Free Software Foundation, Inc.,
   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
   ----------------------------------------------------------------------------- */

define(["jquery"],
       function($){


	   // Global settings object
	   var $this;

	   function change_tab(tabname, containers) {

	   }

	   // YaTabs methods
	   var methods = {
	       init : function( options ) {

		   var settings = $.extend({
		       'active_class': 'active',
		       'container_class': "tabcontainer",
		       'tab_class': "tab",
		       'fadespeed': 'slow',
		       'before_change': function(){},
		       'after_change': function(){},
		       'use_href': true
		   }, options);

		   var containers = $("." + settings.container_class);
		   var tabs = $this.find("." + settings.tab_class);
		   containers.hide();

		   if (settings.use_href) {
		       containers.filter(tabs.filter("." + settings.active_class).find("a").attr("href")).show();
		   }
		   else {
		       containers.filter(tabs.filter("." + settings.active_class).find("a").data("target")).show();
		   }

		   $(tabs).on("click", function(){
		       if (settings.use_href) {
			   var tabname = new String($(this).find("a").attr("href").replace("#", ""));
			   tabs.removeClass(settings.active_class);
			   tabs.find('a').removeClass("active");
			   tabs.find('a[href="#' + tabname + '"]').parent("li." + settings.tab_class).addClass(settings.active_class);
			   tabs.find('a[href="#' + tabname + '"]').parent("li." + settings.tab_class).find("a").addClass("active");
			   settings.before_change();
			   containers.hide();
			   containers.filter("#" + tabname).show();
			   settings.after_change(tabs.filter("." + settings.active_class));
		       }
		       else {
			   var tabname = new String($(this).find("a").data("target").replace("#", ""));
			   tabs.removeClass(settings.active_class);
			   tabs.find('a').removeClass("active");
			   tabs.find('a[data-target="#' + tabname + '"]').parent("li." + settings.tab_class).addClass(settings.active_class);
			   tabs.find('a[data-target="#' + tabname + '"]').parent("li." + settings.tab_class).find("a").addClass("active");
			   settings.before_change();
			   containers.hide();
			   containers.filter("#" + tabname).show();
			   settings.after_change(tabs.filter("." + settings.active_class));

		       }
		   });

		   return this;

	       },
	       changetab: function(tabname) {
	       }

	   };

	   $.fn.yatabs = function(method) {

	       $this = this;
	       if (methods[method]) {
		   return methods[method].apply(this,
						Array.prototype.slice.call(arguments, 1));

	       }
	       else if (typeof method === 'object' || ! method) {
		   return methods.init.apply(this, arguments);

	       }
	       else {
		   $.error('Method ' +  method + ' does not exist on jQuery.yatabs');
	       }
	       return this;
	   };

       }
      )
