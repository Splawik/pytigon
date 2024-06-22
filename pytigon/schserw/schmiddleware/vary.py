from django.utils.deprecation import MiddlewareMixin


class VaryMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.set_vary = None

    def process_response(self, request, response):
        if request.set_vary is not None:
            response.headers["Vary"] = request.set_vary
        return response
