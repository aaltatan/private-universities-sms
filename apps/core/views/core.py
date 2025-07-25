from django.contrib.messages import error
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from apps.reports.forms import LedgerForm


def index(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    return render(request, "apps/core/index.html")


def dashboard(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    return render(request, "apps/core/dashboard.html")


def messages(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    return render(request, "apps/core/messages.html")


def ledger(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    form = LedgerForm()
    template_name = "apps/core/modal-ledger.html"

    if request.method == "POST":
        form = LedgerForm(request.POST)
        response = HttpResponse(status=200)
        if form.is_valid():
            if request.POST.get("details"):
                return redirect(
                    form.cleaned_data.get("employee").get_absolute_url(),
                )

            ledger_url = form.cleaned_data.get("employee").get_ledger_url()
            response["Hx-Redirect"] = ledger_url

        else:
            response["Hx-Retarget"] = "#no-content"
            response["HX-Reswap"] = "innerHTML"
            error(request, form.errors)
            response["HX-Trigger"] = "messages"

        return response

    response = render(request, template_name, {"form": form})
    response["Hx-Trigger"] = "showmodal"
    return response
