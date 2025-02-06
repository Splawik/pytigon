from django.db import models
from django.contrib import admin
from oauth2_provider.models import Application
from django.core.exceptions import ValidationError


class PytigonOAuth2Application(models.Model):
    """
    Custom OAuth2 application model extending the base Application model.
    Adds a scope field to define the scope of the application.
    """

    app = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Application",
        help_text="The associated OAuth2 application.",
    )
    scope = models.CharField(
        max_length=128,
        verbose_name="Scope",
        help_text="The scope of the OAuth2 application.",
    )

    def clean(self):
        """
        Custom validation to ensure the scope is not empty.
        """
        if not self.scope:
            raise ValidationError({"scope": "Scope cannot be empty."})

    def __str__(self):
        """
        String representation of the model.
        """
        return f"{self.app.name} - {self.scope}"


admin.site.register(PytigonOAuth2Application)
