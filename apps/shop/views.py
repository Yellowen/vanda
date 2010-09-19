# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------
#    Dina Project 
#    Copyright (C) 2010  Dina Project Community
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# ---------------------------------------------------------------------------------


def shopping_cart(request, template_name='shopping_cart.html'):
    cart = get_shopping_cart(request)
    ctx = {'cart': cart}
    return render_to_response(template_name, ctx,
context_instance=RequestContext(request))

def add_to_cart(request, queryset, object_id=None, slug=None,
                slug_field='slug', template_name='add_to_cart.
                html'):

    obj = lookup_object(queryset, object_id, slug, slug_field)
    quantity = request.GET.get('quantity', 1)
    cart = get_shopping_cart(request)
    cart.add_item(obj, quantity)
    update_shopping_cart(request, cart)
    ctx = {'object': obj, 'cart': cart}
    return render_to_response(template_name, ctx,
context_instance=RequestContext(request))


def remove_from_cart(request, cart_item_id,
                     template_name='remove_from_cart.html'):
    cart = get_shopping_cart(request)
    cart.remove_item(cart_item_id)
    update_shopping_cart(request, cart)
    ctx = {'cart': cart}
    return render_to_response(template_name, ctx,
context_instance=RequestContext(request))

def lookup_object(queryset, object_id=None, slug=None, slug_
field=None):
    if object_id is not None:
        obj = queryset.get(pk=object_id)
    elif slug and slug_field:
        kwargs = {slug_field: slug}
        obj = queryset.get(**kwargs)
     else:
         raise Http404
     return obj
def checkout(request, template_name='orders/checkout.html'):
     cart = get_shopping_cart(request)
     googleCart, googleSig = sign_google_cart(cart)
     ctx = {'cart': cart,
               'googleCart': googleCart,
               'googleSig': googleSig,
               'googleMerchantKey': settings.GOOGLE_MERCHANT_KEY,
               'googleMerchantID': settings.GOOGLE_MERCHANT_ID}
     return render_to_response(template_name, ctx,
context_instance=RequestContext(request))

