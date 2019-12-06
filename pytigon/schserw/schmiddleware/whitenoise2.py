from django.conf import settings
from whitenoise.middleware import WhiteNoiseMiddleware

class WhiteNoiseMiddleware2(WhiteNoiseMiddleware):
    def __init__(self, get_response=None, settings=settings):
        WhiteNoiseMiddleware.__init__(self, get_response, settings)
        if self.static_root:
            self.add_files(settings.STATIC_APP_ROOT, prefix=self.static_prefix+"app/")
