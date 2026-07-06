# Pytest tests for VaryMiddleware
import pytest
from django.http import HttpRequest, HttpResponse

from pytigon.schserw.schmiddleware.vary import VaryMiddleware


class CustomGetResponse:
    def __init__(self):
        self.last_request = None

    def __call__(self, request):
        self.last_request = request
        response = HttpResponse()
        response._request = request
        return response


@pytest.fixture
def vary_middleware():
    return VaryMiddleware(CustomGetResponse())


def test_call_initializes_set_vary_to_none(vary_middleware):
    request = HttpRequest()
    response = vary_middleware(request)
    assert vary_middleware.get_response.last_request.set_vary is None
    assert response.status_code == 200


def test_call_with_header_value_on_request(vary_middleware):
    def get_response(request):
        request.set_vary = "Accept-Encoding"
        return HttpResponse()

    mw = VaryMiddleware(get_response)
    request = HttpRequest()
    response = mw(request)
    assert response.headers["Vary"] == "Accept-Encoding"


def test_call_with_none_set_vary(vary_middleware):
    request = HttpRequest()
    response = vary_middleware(request)
    assert "Vary" not in response.headers


def test_call_exception_handling():
    def get_response(request):
        response = HttpResponse()
        del response.headers
        request.set_vary = "User-Agent"
        return response

    mw = VaryMiddleware(get_response)
    request = HttpRequest()
    response = mw(request)
    assert response.status_code == 200
