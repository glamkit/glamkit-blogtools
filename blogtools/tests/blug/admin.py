from django.contrib import admin

from blogtools.admin import EntryAdminBase

from models import BlugEntry



class BlugEntryAdmin(EntryAdminBase, admin.ModelAdmin): # Important: Start with EntryAdminBase.
    fieldsets = (
            ('Metadata', { 'fields': ('title', 'slug', 'pub_date', 'author', 'status', 'is_featured', 'enable_comments') }),
            ('Entry', { 'fields': ('excerpt', 'body') }),
            ('Tagging', { 'fields': ('tags',) }),
        )
    list_display = ('title', 'pub_date', 'author', 'status', 'is_featured', 'enable_comments',)
    list_filter = ('status',)

admin.site.register(BlugEntry, BlugEntryAdmin)
