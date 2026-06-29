"""Pytest tests for pytigon.schserw.schmiddleware.csrf module.
"""

from django.http import HttpRequest, HttpResponse

from pytigon.schserw.schmiddleware.csrf import DisableCSRF


class TestDisableCSRF:
    def test_process_request_sets_csrf_flag(self):
        """Test that process_request sets _dont_enforce_csrf_checks."""
        request = HttpRequest()
        middleware = DisableCSRF(lambda req: HttpResponse("OK"))
        response = middleware(request)
        assert response.status_code == 200
        assert getattr(request, "_dont_enforce_csrf_checks", None) is True

    def test_multiple_calls_dont_raise(self):
        """Test that multiple calls to process_request don't raise errors."""
        request = HttpRequest()
        middleware = DisableCSRF(lambda req: HttpResponse("OK"))
        middleware(request)
        middleware(request)  # Should not raise
        assert getattr(request, "_dont_enforce_csrf_checks", None) is True


def test_disable_csrf_function():
    """Test DisableCSRF as a standalone callable."""
    request = HttpRequest()
    response = HttpResponse("OK")

    middleware = DisableCSRF(lambda req: response)
    result = middleware(request)
    assert result.status_code == 200
    assert result is response
