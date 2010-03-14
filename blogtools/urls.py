from django.conf.urls.defaults import *
from django.views.generic import list_detail


from tagging.models import Tag
from tagging.views import tagged_object_list


class UrlPatternsBase(object):
    url_name_root = None
    admin_prefix = 'admin' #TODO: This is probably not right to use something like that to figure out the admin url path. Maybe use the reverse function?
    views = None
    feeds = None


class EntryUrlPatternsMixin(object):
    
    def get_entry_url_patterns(self):
        return self.get_archive_url_patterns() + self.get_feeds_url_patterns() + self.get_other_url_patterns()
    
    def get_archive_url_patterns(self):
        return patterns('',
                url(r'^$',
                    self.views.archive_index,
                    name='%s_entry_archive_index' % self.url_name_root),
               
                url(r'^(?P<year>\d{4})/$',
                    self.views.archive_year,
                    name='%s_entry_archive_year' % self.url_name_root),
                   
                url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
                    self.views.archive_month,
                    name='%s_entry_archive_month' % self.url_name_root),
                   
                url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
                    self.views.archive_day,
                    name='%s_entry_archive_day' % self.url_name_root),
                   
                url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
                    self.views.entry_detail,
                    name='%s_entry_detail' % self.url_name_root),
            )
       
    def get_feeds_url_patterns(self):
        urlpatterns = patterns('',)
        if self.feeds is not None:
            for url_pattern, url_name, feed_view in self.feeds:
                urlpatterns += patterns('',
                         url(url_pattern, feed_view, name='%s_%s' % (self.url_name_root, url_name)),
                     )
        return urlpatterns
        
    def get_other_url_patterns(self): #TODO: rename, and maybe split out the urls in different methods
        return patterns('',
                url(r'^entry_preview/(?P<entry_pk>[0-9]+)/$',
                    self.views.entry_preview,
                    name='%s_entry_preview' % self.url_name_root),
            
                url(r'^search/', self.views.search, name='%s_search' % self.url_name_root),
            )
    
    

class TagUrlPatternsMixin(object):
    
    def get_tag_urlpatterns(self):
        return patterns('',
           url(r'^%s/tag_list/$' % self.admin_prefix, self.views.json_tag_list),
        
           url(r'^tags/$',
               self.views.tag_list,
               name='%s_tag_list' % self.url_name_root),
               
           url(r'^tags/(?P<tag>[-\w]+)/$',
               self.views.tagged_entry_list,
               name='%s_tag_detail' % self.url_name_root),
        )