# django_min_init – Minimal Django Initialization

Lightweight Django setup for scripts and embedded environments without
loading the full `manage.py` machinery. Configures `DJANGO_SETTINGS_MODULE`,
populates apps, and optionally boots the embedded HTTP server.

`init(prj, pytigon_standard=False, embeded_django=False, settings_callback=None)`
clears `DATABASES`, `MIDDLEWARE`, and `INSTALLED_APPS` by default — pass
`pytigon_standard=True` to keep the project's full settings.

::: pytigon.django_min_init
    options:
      show_submodules: false
      members: true
