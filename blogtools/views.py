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
    publication_date_field = 'pub_date'
    slug_field = 'slug'


    def archive_index(self, request, *args, **kwargs):
        if 'entry_queryset' in kwargs:
            queryset = kwargs['entry_queryset']
            del kwargs['entry_queryset']
        else:
            queryset = self.entry_queryset
        info_dict = {
                 'queryset': queryset,
                 'template_name': '%s/entry_archive_index.html' % self.template_root_path,
                 'template_object_name': 'entry',
             }
        return list_detail.object_list(request, *args, **dict(info_dict, **kwargs))

    def archive_year(self, request, *args, **kwargs):
        if 'entry_queryset' in kwargs:
            queryset = kwargs['entry_queryset']
            del kwargs['entry_queryset']
        else:
            queryset = self.entry_queryset
        info_dict = {
                'queryset': queryset,
                'date_field': self.publication_date_field,
                'template_name': '%s/entry_archive_year.html' % self.template_root_path,
                'template_object_name': 'entry',
            }
        return date_based.archive_year(request, *args, **dict(info_dict, make_object_list=True, **kwargs))

    def archive_month(self, request, *args, **kwargs):
        if 'entry_queryset' in kwargs:
            queryset = kwargs['entry_queryset']
            del kwargs['entry_queryset']
        else:
            queryset = self.entry_queryset
        info_dict = {
                'queryset': queryset,
                'date_field': self.publication_date_field,
                'template_name': '%s/entry_archive_month.html' % self.template_root_path,
                'template_object_name': 'entry',
            }
        return date_based.archive_month(request, *args, **dict(info_dict, month_format='%m', **kwargs))

    def archive_day(self, request, *args, **kwargs):
        if 'entry_queryset' in kwargs:
            queryset = kwargs['entry_queryset']
            del kwargs['entry_queryset']
        else:
            queryset = self.entry_queryset
        info_dict = {
                'queryset': queryset,
                'date_field': self.publication_date_field,
                'template_name': '%s/entry_archive_day.html' % self.template_root_path,
                'template_object_name': 'entry',
            }
        return date_based.archive_day(request, *args, **dict(info_dict, month_format='%m', **kwargs))

    def entry_detail(self, request, *args, **kwargs):
        if 'entry_queryset' in kwargs:
            queryset = kwargs['entry_queryset']
            del kwargs['entry_queryset']
        else:
            queryset = self.entry_queryset
        info_dict = {
                'queryset': queryset,
                'date_field': self.publication_date_field,
                'template_name': '%s/entry_detail.html' % self.template_root_path,
                'template_object_name': 'entry',
            }
        return date_based.object_detail(request, *args, **dict(info_dict, month_format='%m', slug_field=self.slug_field, **kwargs))

    def search(self, request, *args, **kwargs):
        if 'entry_queryset' in kwargs:
            queryset = kwargs['entry_queryset']
            del kwargs['entry_queryset']
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
        if 'extra_context' in kwargs:
            context.update(kwargs['extra_context'] or {})

        return render_to_response('%s/search_results.html' % self.template_root_path,
                              context,
                              context_instance=RequestContext(request))

    def entry_preview(self, request, entry_pk, *args, **kwargs):
        @staff_member_required
        def func(request, entry_pk, *args, **kwargs):
            if 'entry_queryset' in kwargs:
                queryset = kwargs['entry_queryset']
                del kwargs['entry_queryset']
            else:
                queryset = self.entry_queryset
            context = {
                'preview': True
            }
            if 'extra_context' in kwargs:
                context.update(kwargs['extra_context'] or {})
            return list_detail.object_detail(
                     request,
                     object_id=entry_pk,
                     queryset=queryset,
                     template_object_name='entry',
                     template_name='%s/entry_detail.html' % self.template_root_path,
                     extra_context=context
                 )
        return func(request, entry_pk, *args, **kwargs)

try:
    from tagging.models import Tag
    from tagging.views import tagged_object_list

    class TaggedEntryViewsMixin(object):

        def tag_list(self, request, *args, **kwargs):
            extra_context = {}
            if 'extra_context' in kwargs:
                extra_context.update(kwargs['extra_context'] or {})
            return list_detail.object_list(
               { 'queryset': Tag.objects.all().order_by('name'),
                 'template_name': '%s/tag_list.html' % self.template_root_path,
                 'template_object_name': 'tag',
                 'extra_context': extra_context }
            )

        def tagged_entry_list(self, request, *args, **kwargs):
            if 'entry_queryset' in kwargs:
                queryset = kwargs['entry_queryset']
                del kwargs['entry_queryset']
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
