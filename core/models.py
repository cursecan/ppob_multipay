from django.db import models


class CommonBase(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    delete = models.DateTimeField(blank=True, null=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True