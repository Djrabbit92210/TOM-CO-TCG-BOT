"""Fnac response summary + capture analysis."""

from __future__ import annotations

from pathlib import Path

from sites.fnac.capture_tools import analyze_capture, load_capture_file, write_sidecar_report
from sites.fnac.response_summary import summarize_fnac_response


def test_summarize_json_body() -> None:
    s = summarize_fnac_response(200, '{"ok":true}', body=None)
    assert s["kind"] == "json"
    assert s["data"]["ok"] is True


def test_summarize_html_cart() -> None:
    html = "<html><title>Panier | fnac</title></html>"
    s = summarize_fnac_response(200, html)
    assert s["kind"] == "html_cart_page"


def test_summarize_maintenance() -> None:
    html = "<html><title>FNAC DARTY - Maintenance</title></html>"
    s = summarize_fnac_response(403, html)
    assert s["kind"] == "maintenance_or_block"


def test_analyze_capture() -> None:
    rows = [
        {
            "method": "POST",
            "url": "https://www.fnac.com/basket/add",
            "postData": "[{}]",
            "status": 200,
            "contentType": "application/json",
        },
        {
            "method": "GET",
            "url": "https://www.fnac.com/basket/summary",
            "status": 200,
            "contentType": "application/json",
        },
    ]
    rep = analyze_capture(rows)
    assert rep["total_rows"] == 2
    assert rep["unique_urls"] == 2
    assert "POST" in rep["methods"]
    assert "200" in rep["statuses"]
    assert len(rep["likely_structured_endpoints"]) >= 1


def test_write_sidecar_report(tmp_path: Path) -> None:
    cap = tmp_path / "fnac_api_capture.json"
    cap.write_text("[]", encoding="utf-8")
    write_sidecar_report(cap, [])
    report = cap.with_suffix(".report.json")
    assert report.is_file()
    assert load_capture_file(cap) == []
