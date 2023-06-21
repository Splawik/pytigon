from oauth2_provider.views.base import TokenView
from oauth2_provider.signals import app_authorized


class ApplicationScopesTokenView(TokenView):
    def post(self, request, *args, **kwargs):
        url, headers, body, status = self.create_token_response(request)
        if status == 200:
            json_body = json.loads(body)
            access_token = json_body.get("access_token")
            if access_token is not None:
                token = get_access_token_model().objects.get(token=access_token)

                if (
                    token.application.pytigonoauth2application
                    and token.application.pytigonoauth2application.scope
                ):
                    token.scope = token.application.pytigonoauth2application.scope
                    token.save()

                    json_body["scope"] = token.scope
                    body = json.dumps(json_body)

                app_authorized.send(sender=self, request=request, token=token)

        response = HttpResponse(content=body, status=status)

        for k, v in headers.items():
            response[k] = v
        return response
