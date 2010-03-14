from django.template import Library

from blogtools.templatetags.blogtools_tags import EntryTemplateTagsBase

from ..models import BlugEntry


register = Library()


class MyEntryTemplateTags(EntryTemplateTagsBase):
    entry_queryset = BlugEntry.objects.live()
    template_root_path = 'blug'

tags = MyEntryTemplateTags()
tags.register(register)