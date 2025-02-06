from pytigon.schserw.schmiddleware.schpost import *

# Pytest tests
import pytest
from django.http import HttpRequest, HttpResponse


def test_view_requests():
    """Test ViewRequests class."""
    request = HttpRequest()
    request.method = "GET"
    request.path = "/test"

    view = ViewRequests()
    view.process_request(request)


def test_view_post_middleware():
    """Test view_post middleware."""
    request = HttpRequest()
    request.method = "POST"
    request.path = "/test"
    request.POST = {"key": "value"}

    def get_response(req):
        return HttpResponse("OK")

    middleware = view_post(get_response)
    response = middleware(request)

    assert response.status_code == 200


def test_view_post_class():
    """Test ViewPost class."""
    request = HttpRequest()
    request.method = "POST"
    request.path = "/test"
    request.POST = {"key": "value"}

    view = ViewPost()
    view.process_request(request)


if __name__ == "__main__":
    pytest.main()
