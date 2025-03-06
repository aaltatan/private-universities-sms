import threading

from django.contrib.auth.middleware import LoginRequiredMiddleware
from django.http import HttpRequest

_request_local = threading.local()


class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _request_local.request = request
        response = self.get_response(request)
        return response

    @staticmethod
    def get_current_request() -> HttpRequest | None:
        """Retrieve the current request object from thread-local storage."""
        return getattr(_request_local, "request", None)


class CustomLoginRequiredMiddleware(LoginRequiredMiddleware):
    def process_view(
        self,
        request: HttpRequest,
        view_func,
        view_args,
        view_kwargs,
    ):
        if request.get_full_path().startswith("/api"):
            return None

        return super().process_view(
            request,
            view_func,
            view_args,
            view_kwargs,
        )
