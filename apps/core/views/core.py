from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@login_required
def index(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    return render(request, "apps/core/index.html")


@login_required
def messages(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    return render(request, "apps/core/messages.html")
