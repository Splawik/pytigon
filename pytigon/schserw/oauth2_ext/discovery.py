"""RFC 8414 OAuth 2.0 Authorization Server Metadata discovery (OAuth 2.1).

Serves the well-known metadata document that lets OAuth 2.1/OIDC clients
discover the authorization server endpoints (authorize, token, revocation,
introspection, JWKS, supported scopes/grants, PKCE, etc.).

Default metadata can be tuned with an optional ``OAUTH2_PROVIDER_DISCOVERY``
dictionary in Django settings, e.g.::

    OAUTH2_PROVIDER_DISCOVERY = {
        "GRANT_TYPES_SUPPORTED": ["authorization_code", "client_credentials"],
        "RESPONSE_TYPES_SUPPORTED": ["code"],
    }
"""

import logging

from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from oauth2_provider.compat import login_not_required
from oauth2_provider.models import AbstractGrant
from oauth2_provider.settings import oauth2_settings

logger = logging.getLogger(__name__)

DEFAULT_METADATA = {
    "GRANT_TYPES_SUPPORTED": [
        "authorization_code",
        "client_credentials",
        "refresh_token",
        "urn:ietf:params:oauth:grant-type:device_code",
    ],
    "RESPONSE_TYPES_SUPPORTED": ["code"],
    "RESPONSE_MODES_SUPPORTED": ["query", "fragment"],
    "TOKEN_ENDPOINT_AUTH_METHODS_SUPPORTED": [
        "client_secret_post",
        "client_secret_basic",
    ],
    "SCOPES_SUPPORTED": ["read", "write"],
    "CODE_CHALLENGE_METHODS_SUPPORTED": ["S256", "plain"],
}


def _option(name):
    """Read an optional override from OAUTH2_PROVIDER_DISCOVERY, else default."""
    user = getattr(settings, "OAUTH2_PROVIDER_DISCOVERY", {}) or {}
    return user.get(name, DEFAULT_METADATA[name])


@method_decorator(login_not_required, name="dispatch")
class OAuth2AuthorizationServerMetadataView(View):
    """Serve the RFC 8414 OAuth 2.0 Authorization Server Metadata document."""

    def get(self, request, *args, **kwargs):
        data = self._build_metadata(request)
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        response["Cache-Control"] = "public, max-age=86400"
        return response

    def _resolve(self, request, name):
        """Build an absolute URL for a named oauth2_provider endpoint."""
        if oauth2_settings.OIDC_ISS_ENDPOINT:
            parsed = oauth2_settings.OIDC_ISS_ENDPOINT.rstrip("/")
            return f"{parsed}{reverse(name)}"
        return request.build_absolute_uri(reverse(name))

    def _build_metadata(self, request):
        issuer = oauth2_settings.oidc_issuer(request).rstrip("/")

        code_challenge_methods = _option("CODE_CHALLENGE_METHODS_SUPPORTED")
        if not code_challenge_methods:
            code_challenge_methods = list(dict(AbstractGrant.CODE_CHALLENGE_METHODS).keys())

        metadata = {
            "issuer": issuer,
            "authorization_endpoint": self._resolve(request, "oauth2_provider:authorize"),
            "token_endpoint": self._resolve(request, "oauth2_provider:token"),
            "jwks_uri": self._resolve(request, "oauth2_provider:jwks-info"),
            "scopes_supported": sorted(_option("SCOPES_SUPPORTED")),
            "response_types_supported": _option("RESPONSE_TYPES_SUPPORTED"),
            "response_modes_supported": _option("RESPONSE_MODES_SUPPORTED"),
            "grant_types_supported": _option("GRANT_TYPES_SUPPORTED"),
            "token_endpoint_auth_methods_supported": _option(
                "TOKEN_ENDPOINT_AUTH_METHODS_SUPPORTED"
            ),
            "revocation_endpoint": self._resolve(request, "oauth2_provider:revoke-token"),
            "introspection_endpoint": self._resolve(request, "oauth2_provider:introspect"),
            "code_challenge_methods_supported": code_challenge_methods,
        }

        device_endpoint = self._resolve(request, "oauth2_provider:device-authorization")
        metadata["device_authorization_endpoint"] = device_endpoint

        if oauth2_settings.OIDC_RP_INITIATED_LOGOUT_ENABLED:
            metadata["end_session_endpoint"] = self._resolve(
                request, "oauth2_provider:rp-initiated-logout"
            )

        return metadata
