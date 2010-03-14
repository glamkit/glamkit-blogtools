from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.conf import settings


class EntryFeedBase(Feed):
    # Custom parameters
    blog_name = None
    entry_queryset = None
    url_name_root = None

    def item_pubdate(self, item):
        return item.pub_date

class Entries(EntryFeedBase):

    def link(self, obj):
        return reverse('%s_entry_archive_index' % self.url_name_root)

    def title(self, obj):
        return self.blog_name

    def items(self):
        return self.entry_queryset[:10]
    

try:
    from tagging.models import Tag, TaggedItem

    class EntriesByTag(EntryFeedBase):  #TODO: Maybe this should be a mixin that doesn't inherit from anything.
    
        def get_object(self, request, tag_name):
            return Tag.objects.get(name=tag_name)
    
        def title(self, obj):
            return "%s: Entries tagged with '%s'" % (self.blog_name, obj.name)
    
        def link(self, obj):
            return reverse('%s_tag_detail' % self.url_name_root, args=[obj.name])
    
        def items(self, obj):
            return TaggedItem.objects.get_by_model(self.entry_queryset, obj)[:10]
except ImportError:
    pass