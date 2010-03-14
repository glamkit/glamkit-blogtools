class EntryAdminBase(object):
    date_hierarchy = 'pub_date'
    search_fields = ('excerpt', 'body', 'title',)
    ordering = ['-pub_date']
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True    
