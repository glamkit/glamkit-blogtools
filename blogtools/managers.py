from django.db import models


class StatusEntryManager(models.Manager):
    def live(self):
        return self.filter(status__exact=self.model.LIVE_STATUS)
        
    def draft_and_live(self):
        return self.filter(status__in=[self.model.LIVE_STATUS, self.model.DRAFT_STATUS])
    