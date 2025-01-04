from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "apps/core/index.html")


def messages(request: HttpRequest) -> HttpResponse:
    return render(request, "apps/core/messages.html")