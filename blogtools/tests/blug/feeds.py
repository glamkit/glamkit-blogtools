from blogtools import feeds

from models import BlugEntry

class Entries(feeds.Entries):
    blog_name = 'My blog'
    entry_queryset = BlugEntry.objects.live()
    url_name_root = 'blug'

class EntriesByTag(feeds.EntriesByTag):
    blog_name = 'My blog'
    entry_queryset = BlugEntry.objects.live()
    url_name_root = 'blug'
