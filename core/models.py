from django.db import models


class LogTable(models.Model):
    url = models.CharField(max_length=255)
    status_code = models.IntegerField()
    duration = models.DurationField()
    now = models.DateTimeField()
    index = models.IntegerField()
