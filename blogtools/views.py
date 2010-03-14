import datetime

from django.shortcuts import get_object_or_404
from django.views.generic import date_based, list_detail
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.syndication.views import feed as django_feed

from utils import get_query




class BaseEntryViews(object):
    entry_queryset = None
    template_root_path = None        

    def archive_index(self, request, entry_queryset=None, *args, **kwargs):
        if entry_queryset is not None:
            queryset = entry_queryset
        else:
            queryset = self.entry_queryset
        info_dict = {
                 'queryset': queryset,
                 'template_name': '%s/entry_archive_index.html' % self.template_root_path,
                 'template_object_name': 'entry',
             }
        return list_detail.object_list(request, *args, **dict(info_dict, **kwargs))

    def archive_year(self, request, entry_queryset=None, *args, **kwargs):
        if entry_queryset is not None:
            queryset = entry_queryset
        else:
            queryset = self.entry_queryset
        info_dict = {
                'queryset': queryset,
                'date_field': 'pub_date',
                'template_name': '%s/entry_archive_year.html' % self.template_root_path,
                'template_object_name': 'entry',
            }
        return date_based.archive_year(request, *args, **dict(info_dict, make_object_list=True, **kwargs))

    def archive_month(self, request, entry_queryset=None, *args, **kwargs):
        if entry_queryset is not None:
            queryset = entry_queryset
        else:
            queryset = self.entry_queryset
        info_dict = {
                'queryset': queryset,
                'date_field': 'pub_date',
                'template_name': '%s/entry_archive_month.html' % self.template_root_path,
                'template_object_name': 'entry',
            }
        return date_based.archive_month(request, *args, **dict(info_dict, month_format='%m', **kwargs))
    
    def archive_day(self, request, entry_queryset=None, *args, **kwargs):
        if entry_queryset is not None:
            queryset = entry_queryset
        else:
            queryset = self.entry_queryset
        info_dict = {
                'queryset': queryset,
                'date_field': 'pub_date',
                'template_name': '%s/entry_archive_day.html' % self.template_root_path,
                'template_object_name': 'entry',
            }
        return date_based.archive_day(request, *args, **dict(info_dict, month_format='%m', **kwargs))

    def entry_detail(self, request, entry_queryset=None, *args, **kwargs):
        if entry_queryset is not None:
            queryset = entry_queryset
        else:
            queryset = self.entry_queryset
        info_dict = {
                'queryset': queryset,
                'date_field': 'pub_date',
                'template_name': '%s/entry_detail.html' % self.template_root_path,
                'template_object_name': 'entry',
            }
        return date_based.object_detail(request, *args, **dict(info_dict, month_format='%m', slug_field='slug', **kwargs))
       
    def search(self, request, entry_queryset=None, extra_context=None):
        if entry_queryset is not None:
            queryset = entry_queryset
        else:
            queryset = self.entry_queryset
        query_string = ''
        found_entries = None
        if ('q' in request.GET) and request.GET['q'].strip():
            query_string = request.GET['q']
            
            entry_query = get_query(query_string, ['title', 'body',])
            
            found_entries = queryset.filter(entry_query)
    
        context = {
            'query_string': query_string,
            'found_entries': found_entries
        }
        context.update(extra_context or {})
    
        return render_to_response('%s/search_results.html' % self.template_root_path,
                              context,
                              context_instance=RequestContext(request))
    
    def entry_preview(self, request, entry_pk, entry_queryset=None, extra_context=None):
        if entry_queryset is not None:
            queryset = entry_queryset
        else:
            queryset = self.entry_queryset
        @staff_member_required
        def func(request, entry_pk, extra_context=None):
            context = {
                'preview': True
            }
            context.update(extra_context or {})
            return list_detail.object_detail(
                     request, 
                     object_id=entry_pk,
                     queryset=queryset,
                     template_object_name='entry',
                     template_name='%s/entry_detail.html' % self.template_root_path,
                     extra_context=context
                 )
        return func(request, entry_pk, extra_context)

try:
    from tagging.models import Tag
    from tagging.views import tagged_object_list
    
    class TaggedEntryViewsMixin(object):
    
        def tag_list(self, request, extra_context=None):
            return list_detail.object_list(
               { 'queryset': Tag.objects.all().order_by('name'),
                 'template_name': '%s/tag_list.html' % self.template_root_path,
                 'template_object_name': 'tag',
                 'extra_context': extra_context }
            )
        
        def tagged_entry_list(self, request, entry_queryset=None, *args, **kwargs):
            if entry_queryset is not None:
                queryset = entry_queryset
            else:
                queryset = self.entry_queryset
            info_dict = {
                 'queryset_or_model': queryset,
                 'template_name': '%s/tag_detail.html' % self.template_root_path,
                 'template_object_name': 'entry',
                 }
            return tagged_object_list(request, *args, **dict(info_dict, **kwargs))
        
        def json_tag_list(self, request):
            tags = [tag.name for tag in Tag.objects.all()]
            json = simplejson.dumps({ 'success': True, 'tags': tags })
            return HttpResponse(json, mimetype='text/plain')
except ImportError:
    pass