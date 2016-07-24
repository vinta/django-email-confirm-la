from __future__ import unicode_literals

from django.db import models


class YourModel(models.Model):
    customer_support_email = models.EmailField(null=True, blank=True)
    marketing_email = models.EmailField(null=True, blank=True)
