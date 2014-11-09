# coding: utf-8

from django.db import models


class YourModel(models.Model):
    customer_support_email = models.EmailField(max_length=255, null=True, blank=True)
    marketing_email = models.EmailField(max_length=255, null=True, blank=True)
