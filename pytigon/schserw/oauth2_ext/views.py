"""Custom OAuth2 token view with application-specific scope handling.

Extends the base TokenView from django-oauth-toolkit to support
application-level scope overrides via the PytigonOAuth2Application model.
"""

import json
import logging

from django.http import HttpResponse
from oauth2_provider.models import get_access_token_model
from oauth2_provider.signals import app_authorized
from oauth2_provider.views.base import TokenView

logger = logging.getLogger(__name__)

# Get the AccessToken model's DoesNotExist exception for catching missing tokens
AccessToken = get_access_token_model()
AccessTokenDoesNotExist = AccessToken.DoesNotExist


class ApplicationScopesTokenView(TokenView):
    """Custom TokenView that applies application-specific OAuth2 scopes.

    When an application has a PytigonOAuth2Application with a custom scope,
    the issued token's scope is overridden with that application-specific scope.
    """

    def post(self, request, *args, **kwargs):
        """Handle POST request to create a token, applying app-specific scopes.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: JSON response with the token data.
        """
        try:
            # Create the initial token response from the parent class
            url, headers, body, status = self.create_token_response(request)

            if status == 200:
                json_body = json.loads(body)
                access_token = json_body.get("access_token")

                if access_token:
                    token = AccessToken.objects.get(token=access_token)

                    # Check if the application has custom scopes
                    if (
                        hasattr(token.application, "pytigonoauth2application")
                        and token.application.pytigonoauth2application.scope
                    ):
                        token.scope = token.application.pytigonoauth2application.scope
                        token.save()

                        # Update the response body with the new scope
                        json_body["scope"] = token.scope
                        body = json.dumps(json_body)

                    # Send the app_authorized signal
                    app_authorized.send(sender=self, request=request, token=token)

            # Create the final HTTP response
            response = HttpResponse(content=body, status=status)
            for k, v in headers.items():
                response[k] = v

            return response

        except json.JSONDecodeError:
            logger.warning("Invalid JSON in token response", exc_info=True)
            return HttpResponse(
                content='{"error": "Invalid JSON in response"}', status=400
            )
        except AccessTokenDoesNotExist:
            logger.warning("Access token not found after creation")
            return HttpResponse(content='{"error": "Token not found"}', status=404)
        except Exception as e:
            logger.error("Error in token view: %s", e, exc_info=True)
            return HttpResponse(
                content='{"error": "Internal server error"}', status=500
            )
