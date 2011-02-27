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


from django.db import models
from django.contrib.auth.models import User

class Catalog(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=150)
    publisher = models.CharField(max_length=300)
    description = models.TextField()
    pub_date = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return "%s" % self.name
        
class Product(models.Model):
    category = models.ForeignKey('CatalogCategory',
                             related_name='products')
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=150)
    description = models.TextField()
    photo = models.ImageField(upload_to='product_photo',
                              blank=True)
    manufacturer = models.CharField(max_length=300,
                                     blank=True)
    price_in_dollars = models.DecimalField(max_digits=6,
                                            decimal_places=2)

class CatalogCategory(models.Model):
    catalog = models.ForeignKey('Catalog',
                                 related_name='categories')
    parent = models.ForeignKey('self', blank=True, null=True,
                                related_name='children')
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=150)
    description = models.TextField(blank=True)

    def __unicode__(self):
        if self.parent:
            return u'%s: %s - %s' % (self.catalog.name,
                                 self.parent.name,
                                 self.name)
            return u'%s: %s' % (self.catalog.name, self.name)


class ProductAttribute(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    def __unicode__(self):
        return u'%s' % self.name


class ProductDetail(models.Model):
    product = models.ForeignKey('Product',
                                 related_name='details')
    attribute = models.ForeignKey('ProductAttribute')
    value = models.CharField(max_length=500)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return u'%s: %s - %s' % (self.product,
                                 self.attribute,
                                 self.value)

class Customer(models.Model):
    user = models.ForeignKey(User)
    address = models.ForeignKey('CustomerAddress')
    phone_number = PhoneNumberField(blank=True)

class CustomerAddress(models.Model):
    line_1 = models.CharField(max_length=300)
    line_2 = models.CharField(max_length=300)
    line_3 = models.CharField(max_length=300)
    city = models.CharField(max_length=150)
    postalcode = models.CharField(max_length=10)
    state = USStateField(blank=True)
    country = models.CharField(max_length=150)

class Order(models.Model):
    customer = models.ForeignKey(User, blank=True, null=True)
    status_code = models.ForeignKey('StatusCode')
    date_placed = models.DateTimeField()
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    comments = models.TextField(blank=True)
    products = models.ManyToManyField(Product,
                                      through='ProductInOrder')

class StatusCode(models.Model):
    short_name = models.CharField(max_length=10)
    name = models.CharField(max_length=300)
    description = models.TextField()

class ProductInOrder(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField()
    comments = models.TextField(blank=True)
