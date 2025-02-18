from datetime import datetime

from django.test import Client


class CommonExportTests:
    @staticmethod
    def test_export_response_without_permission(
        client: Client,
        urls: dict[str, str],
        headers_modal_GET: dict[str, str],
        subapp_label: str,
    ) -> None:
        client.login(
            username=f"{subapp_label}_user_with_view_perm_only",
            password="password",
        )
        url = urls["index"] + "?export=true&extension=xlsx&redirected=true"
        response = client.get(url, headers=headers_modal_GET)

        assert response.status_code == 403

    @staticmethod
    def test_export_response(
        admin_client: Client,
        urls: dict[str, str],
        headers_modal_GET: dict[str, str],
        filename: str,
        export_test_cases: tuple[str, str],
    ) -> None:
        extension, content_type = export_test_cases

        url = urls["index"] + f"?export=true&extension={extension}"

        response = admin_client.get(url, headers=headers_modal_GET)

        assert response.status_code == 200
        assert "HX-Redirect" in response.headers

        url += "&redirected=true"
        response = admin_client.get(url, headers=headers_modal_GET)

        assert response.status_code == 200
        assert response.headers["Content-Type"] == content_type

        str_now_without_sec = datetime.now().strftime("%Y-%m-%d-%H-%M")
        filename_without_sec = f"{filename}-{str_now_without_sec}"

        assert filename_without_sec in response.headers["Content-Disposition"]
