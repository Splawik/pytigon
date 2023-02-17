from pytigon_lib.schdjangoext.rest_tools import create_api_for_models
from . import models

urlpatterns = []
create_api_for_models(models, urlpatterns)
