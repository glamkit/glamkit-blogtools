from blogtools.views import BaseEntryViews, TaggedEntryViewsMixin

from models import BlugEntry

class MyViews(BaseEntryViews, TaggedEntryViewsMixin):
    entry_queryset = BlugEntry.objects.live()
    template_root_path = 'blug'