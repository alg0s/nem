# author: goodalg0s@gmail.com

from django.db import models


class NemFile(models.Model):
    name = models.CharField(max_length=400, blank=False, unique=True)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
