from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
import logging

LOGGER = logging.getLogger("pytigon")

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def authentication_error(self, request, provider_id, error, exception, extra_context):
        error_dict = {
            'title': 'SocialAccount authentication error!',
            'provider_id': provider_id,
            'error': error.__str__(),
            'exception': exception.__str__(),
            'extra_context': extra_context,
        }
        LOGGER.error(error_dict)
