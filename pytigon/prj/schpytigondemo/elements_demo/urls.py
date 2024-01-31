from django.utils.translation import gettext_lazy as _
from pytigon_lib.schviews import generic_table_start
from . import views

urlpatterns = []

gen = generic_table_start(urlpatterns, "elements_demo", views)


gen.standard("DemoDocHead", _("Demo document head"), _("Demo document heads"))
gen.standard("DemoDocItem", _("Demo document item"), _("Demo document items"))
