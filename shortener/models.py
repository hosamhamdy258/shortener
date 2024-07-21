from django.db import models
from django.utils.translation import gettext_lazy as _

class Shortener(models.Model):
    target_url = models.CharField(_("Original Url"), max_length=1024)
    short_url = models.CharField(_("Shorted Url"), max_length=50)
    created = models.DateTimeField(_("Created Time"), auto_now_add=True)