from oauth2_provider.models import Application
from django.db import models
from django.contrib import admin


class PytigonOAuth2Application(models.Model):
    app = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    scope = models.CharField(max_length=128)


admin.site.register(PytigonOAuth2Application)
