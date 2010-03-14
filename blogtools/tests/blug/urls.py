from blogtools.urls import UrlPatternsBase, EntryUrlPatternsMixin, TagUrlPatternsMixin

from views import MyViews
from feeds import Entries, EntriesByTag

class MyUrlPatterns(UrlPatternsBase, EntryUrlPatternsMixin, TagUrlPatternsMixin):
    url_name_root = 'blug'
    admin_prefix = 'admin'
    views = MyViews()
    feeds = [
            (r'^feeds/latest/', 'feed_latest', Entries()),
            (r'^feeds/tags/(?P<tag_name>.*)/', 'feed_tags', EntriesByTag())
        ]
    
    @property
    def urlpatterns(self):
        return self.get_entry_url_patterns() + self.get_tag_urlpatterns()

urlpatterns = MyUrlPatterns().urlpatterns