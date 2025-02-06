import json
from django.http import HttpResponse
from oauth2_provider.views.base import TokenView
from oauth2_provider.signals import app_authorized
from oauth2_provider.models import get_access_token_model


class ApplicationScopesTokenView(TokenView):
    """
    Custom TokenView that extends the base TokenView to handle application-specific scopes.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to create a token response and modify it based on application scopes.
        """
        try:
            # Create the initial token response
            url, headers, body, status = self.create_token_response(request)

            if status == 200:
                json_body = json.loads(body)
                access_token = json_body.get("access_token")

                if access_token:
                    token = get_access_token_model().objects.get(token=access_token)

                    # Check if the application has custom scopes and update the token accordingly
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
            return HttpResponse(content='{"error": "Invalid JSON"}', status=400)
        except get_access_token_model().DoesNotExist:
            return HttpResponse(content='{"error": "Token not found"}', status=404)
        except Exception as e:
            return HttpResponse(content=f'{{"error": "{str(e)}"}}', status=500)
