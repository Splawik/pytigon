# manage – Django Management Bridge

Django `manage.py` entry point configured to work within pytigon's
path structure and environment. Delegates to `pytigon_lib.schdjangoext.django_manage`
so that `manage_*` CLI commands reuse the same configuration.

::: pytigon.manage
    options:
      show_submodules: false
      members: true
