from django.db import models


class StatusEntryManager(models.Manager):
    def live(self):
        return self.filter(status__exact=self.model.LIVE_STATUS)