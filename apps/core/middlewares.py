from django.contrib.auth.middleware import LoginRequiredMiddleware
from django.http import HttpRequest


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
