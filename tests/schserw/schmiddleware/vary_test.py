from pytigon.schserw.schmiddleware.vary import *

# Pytest tests for VaryMiddleware
import pytest
from django.http import HttpRequest, HttpResponse


@pytest.fixture
def vary_middleware():
    def get_response(request):
        return HttpResponse()

    return VaryMiddleware(get_response)


def test_process_request_sets_set_vary_none(vary_middleware):
    request = HttpRequest()
    vary_middleware.process_request(request)
    assert request.set_vary is None


def test_process_response_with_set_vary(vary_middleware):
    request = HttpRequest()
    request.set_vary = "User-Agent"
    response = HttpResponse()
    response = vary_middleware.process_response(request, response)
    assert response.headers["Vary"] == "User-Agent"


def test_process_response_without_set_vary(vary_middleware):
    request = HttpRequest()
    request.set_vary = None
    response = HttpResponse()
    response = vary_middleware.process_response(request, response)
    assert "Vary" not in response.headers


def test_process_response_exception_handling(vary_middleware):
    request = HttpRequest()
    request.set_vary = "User-Agent"
    response = HttpResponse()
    # Simulate an error by removing the headers attribute
    delattr(response, "headers")
    with pytest.raises(MiddlewareNotUsed):
        vary_middleware.process_response(request, response)
