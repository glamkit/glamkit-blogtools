from blogtools.models import EntryBase, StatusableEntryMixin, FeaturableEntryMixin, HTMLFormattableEntryMixin, TaggableEntryMixin
from blogtools.managers import StatusEntryManager

class BlugEntry(StatusableEntryMixin, FeaturableEntryMixin, HTMLFormattableEntryMixin, TaggableEntryMixin, EntryBase):
    objects = StatusEntryManager()

    template_root_path = 'blug'
    
    class Meta:
        verbose_name_plural = "Entries"