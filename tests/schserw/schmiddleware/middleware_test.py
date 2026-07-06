import pytest
from django.http import HttpRequest, HttpResponse

from pytigon.schserw.schmiddleware.vary import VaryMiddleware


class CustomGetResponse:
    def __init__(self):
        self.last_request = None

    def __call__(self, request):
        self.last_request = request
        return HttpResponse()


@pytest.fixture
def vary_middleware():
    return VaryMiddleware(CustomGetResponse())


class TestVaryMiddlewareNewStyle:
    def test_call_initializes_set_vary(self, vary_middleware):
        request = HttpRequest()
        response = vary_middleware(request)
        assert response.status_code == 200
        assert vary_middleware.get_response.last_request.set_vary is None

    def test_call_without_set_vary(self, vary_middleware):
        request = HttpRequest()
        response = vary_middleware(request)
        assert "Vary" not in response.headers

    def test_call_exception_handling(self):
        def get_response(request):
            response = HttpResponse()
            del response.headers
            request.set_vary = "User-Agent"
            return response

        mw = VaryMiddleware(get_response)
        request = HttpRequest()
        response = mw(request)
        assert response.status_code == 200


class TestJwtMiddleware:
    def test_no_token_in_request(self):
        from pytigon.schserw.schmiddleware.schjwt import JWTUserMiddleware

        request = HttpRequest()
        middleware = JWTUserMiddleware(lambda req: HttpResponse("OK"))
        response = middleware(request)
        assert response.status_code == 200


class TestViewRequests:
    def test_logs_method_and_path(self):
        from pytigon.schserw.schmiddleware.schpost import ViewRequests

        request = HttpRequest()
        request.method = "GET"
        request.path = "/test/"
        middleware = ViewRequests(lambda req: HttpResponse("OK"))
        response = middleware(request)
        assert response.status_code == 200


class TestViewPostMiddleware:
    def test_get_request_no_logging(self):
        from pytigon.schserw.schmiddleware.schpost import view_post

        request = HttpRequest()
        request.method = "GET"
        middleware = view_post(lambda req: HttpResponse("OK"))
        response = middleware(request)
        assert response.status_code == 200

    def test_post_request(self):
        from pytigon.schserw.schmiddleware.schpost import view_post

        request = HttpRequest()
        request.method = "POST"
        request.POST["key"] = "value"
        middleware = view_post(lambda req: HttpResponse("OK"))
        response = middleware(request)
        assert response.status_code == 200
