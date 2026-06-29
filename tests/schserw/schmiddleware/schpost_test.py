# Pytest tests
import pytest
from django.http import HttpRequest, HttpResponse

from pytigon.schserw.schmiddleware.schpost import (
    ViewPost,
    ViewRequests,
    view_post,
)


def test_view_requests():
    """Test ViewRequests class logs request method and path."""
    request = HttpRequest()
    request.method = "GET"
    request.path = "/test"

    view = ViewRequests(lambda req: HttpResponse("OK"))
    response = view(request)
    assert response.status_code == 200


def test_view_post_middleware():
    """Test view_post middleware for POST requests."""
    request = HttpRequest()
    request.method = "POST"
    request.path = "/test"
    request.POST = {"key": "value"}

    def get_response(req):
        return HttpResponse("OK")

    middleware = view_post(get_response)
    response = middleware(request)

    assert response.status_code == 200
    assert response.content == b"OK"


def test_view_post_middleware_get():
    """Test view_post middleware for GET requests."""
    request = HttpRequest()
    request.method = "GET"
    request.path = "/test"

    def get_response(req):
        return HttpResponse("GET OK")

    middleware = view_post(get_response)
    response = middleware(request)

    assert response.status_code == 200
    assert response.content == b"GET OK"


def test_view_post_class():
    """Test ViewPost class processes POST request."""
    request = HttpRequest()
    request.method = "POST"
    request.path = "/test"
    request.POST = {"key": "value"}

    view = ViewPost(lambda req: HttpResponse("OK"))
    response = view(request)
    assert response.status_code == 200


def test_view_post_class_get():
    """Test ViewPost class for GET request (no POST logging)."""
    request = HttpRequest()
    request.method = "GET"
    request.path = "/test"

    view = ViewPost(lambda req: HttpResponse("OK"))
    response = view(request)
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main()
