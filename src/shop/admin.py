# -*- coding: utf-8 -*-
# (c) 2009-2011 Ruslan Popov <ruslan.popov@gmail.com>

from django.conf import settings
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from shop import models

class Category(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'parent')
    search_fields = ('title',)
admin.site.register(models.Category, Category)

class Color(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'colored_field',)
    ordering = ('title',)

    def colored_field(self, floor):
        """ Метод для раскраски поля с цветом. """
        return u'<div style="background-color: %s;">%s</div>' % (floor.color, floor.color)
    colored_field.short_model_desc = _(u'Color')
    colored_field.allow_tags = True

    def formfield_for_dbfield(self, db_field, **kwargs):
        """ Метод для изменения виджета для поля определения цвета. """
        from widgets import ColorPickerWidget
        if db_field.name == 'color':
            kwargs['widget'] = ColorPickerWidget
        return super(Color, self).formfield_for_dbfield(db_field, **kwargs)
admin.site.register(models.Color, Color)

class Country(admin.ModelAdmin):
    list_display = ('iso2', 'iso3', 'title',)
admin.site.register(models.Country, Country)

class Producer(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'country',)
    search_fields = ('title',)
admin.site.register(models.Producer, Producer)

class Item(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Информация',
         {'fields':(('title', 'slug'),
                    ('category', 'producer'),
                    'color', 'price', 'is_present',
                    )}),
        ('Подробности',
         {'fields': ('image', 'desc', 'tags')})
        )
    list_display = ('title', 'get_thumbnail_html', 'category', 'price', 'is_present', 'registered',)
    search_fields = ('title', 'category')
    save_as = True
admin.site.register(models.Item, Item)

class Order(admin.ModelAdmin):
    fieldsets = (
        ('О покупателе',
         {'fields': ('lastname', 'firstname', 'phone')}),
        ('Заказ',
         {'fields': ('totalprice', 'discount', 'count')}),
        ('Доставка',
         {'fields': ('status', 'ship_to', 'comment')})
        )
    list_display = ('lastname', 'firstname', 'phone', 'status', 'totalprice', 'discount', 'registered')
    search_fields = ('lastname', 'firstname', 'status')
admin.site.register(models.Order, Order)

