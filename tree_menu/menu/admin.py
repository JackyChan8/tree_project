from django.contrib import admin

from .models import Menu, Item


class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_filter = ('title', 'slug')
    add_fieldsets = (
        ('Add new item', {
            'description': "Parent should be a menu or item",
            'fields': (('menu', 'parent'), 'title', 'slug')
        }),
    )


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'parent')
    list_filter = ('title', 'slug', 'menu')


admin.site.register(Menu, MenuAdmin)
admin.site.register(Item, ItemAdmin)
