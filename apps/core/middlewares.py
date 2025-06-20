import threading

from django.contrib import messages
from django.contrib.auth.middleware import LoginRequiredMiddleware
from django.http import HttpRequest
from django.utils.safestring import mark_safe


class ExceptionHandlingMiddleware:
    exception = None

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if self.exception:
            messages.error(
                request,
                mark_safe(
                    f"""
                     <span class='font-medium'>
                        Error ({response.status_code}): 
                     </span>
                     <span class='text-lg'>{self.exception}</span>
                    """
                ),
            )
            response["Hx-Trigger"] = "messages"
            self.exception = None
        return response

    def process_exception(self, request, exception):
        self.exception = exception
        return


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
