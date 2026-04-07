"""CLI: python -m sites.fnac add --product-id … | python -m sites.fnac probe"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from accounts.cookie_store import CookieStore
from sites.fnac.buyer import FnacBuyer
from sites.fnac.models import FnacWatchConfig
from sites.fnac.monitor import FnacMonitor


def main() -> int:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--cookies-dir",
        default="./data/cookies",
        help="Directory for fnac.json session cookies",
    )
    common.add_argument("--user-agent", default=None)

    parser = argparse.ArgumentParser(description="Fnac HTTP API client")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", parents=[common], help="POST /basket/add")
    p_add.add_argument("--product-id", required=True)
    p_add.add_argument("--quantity", type=int, default=1)
    p_add.add_argument(
        "--referer-path",
        default="/SearchResult/ResultList.aspx?Search=pokemon&sft=1&sa=0",
        help="Path on www.fnac.com for Referer (leading /)",
    )
    p_add.add_argument("--httpx-only", action="store_true", help="Do not use Playwright fallback")
    p_add.add_argument("--no-headless", action="store_true", help="Show browser (Playwright path)")
    p_add.add_argument("--verbose", "-v", action="store_true", help="Print truncated raw body after summary")

    p_cap = sub.add_parser(
        "capture",
        parents=[common],
        help="Playwright: log XHR/fetch to data/fnac_api_capture.json (Akamai-safe)",
    )
    p_cap.add_argument(
        "--out",
        default="./data/fnac_api_capture.json",
        help="Output JSON path",
    )
    p_cap.add_argument(
        "--referer-path",
        default="/SearchResult/ResultList.aspx?Search=pokemon&sft=1&sa=0",
    )
    p_cap.add_argument("--extra-url", default="", help="Optional extra page to open (full URL or path)")
    p_cap.add_argument(
        "--click-add",
        action="store_true",
        help="Click first 'Ajouter au panier' (fires basket XHR)",
    )
    p_cap.add_argument(
        "--duration",
        type=float,
        default=120.0,
        help="Seconds to keep browser open for manual steps",
    )
    p_cap.add_argument("--settle", type=float, default=3.0, help="Seconds to wait at end")
    p_cap.add_argument("--no-headless", action="store_true", dest="cap_no_headless")

    p_probe = sub.add_parser(
        "probe",
        parents=[common],
        help="GET /basket + inferred JSON routes (refine sites/fnac/endpoints.py)",
    )
    p_probe.add_argument(
        "--referer-path",
        default="/SearchResult/ResultList.aspx?Search=pokemon&sft=1&sa=0",
    )
    p_probe.add_argument(
        "--playwright",
        action="store_true",
        help="Use browser session for GET /basket* (recommended if httpx gets Akamai)",
    )
    p_probe.add_argument("--no-headless", action="store_true", dest="probe_no_headless")

    p_an = sub.add_parser(
        "analyze-capture",
        parents=[common],
        help="Summarize data/fnac_api_capture.json (hosts, methods, POST samples)",
    )
    p_an.add_argument(
        "--in",
        dest="capture_in",
        default="./data/fnac_api_capture.json",
        help="Path to capture JSON from 'capture' command",
    )

    p_list = sub.add_parser("endpoints", parents=[common], help="Print endpoint checklist")

    p_watch = sub.add_parser("watch", parents=[common], help="Poll until in band + in stock, then add")
    p_watch.add_argument("--mode", choices=["search", "url"], required=True)
    p_watch.add_argument("--query", default="", help="Search mode: keywords")
    p_watch.add_argument("--url", default="", help="URL mode: PDP URL")
    p_watch.add_argument("--product-id", default="", dest="watch_product_id")
    p_watch.add_argument("--name-hint", default="")
    p_watch.add_argument("--price-min", type=float, default=None)
    p_watch.add_argument("--price-max", type=float, default=None)
    p_watch.add_argument("--interval", type=float, default=30.0)
    p_watch.add_argument("--max-tries", type=int, default=None)
    p_watch.add_argument("--dry-run", action="store_true", help="Poll only, do not add to cart")
    p_watch.add_argument("--no-headless", action="store_true", help="Show browser for Playwright fetches")

    args = parser.parse_args()

    if args.cmd == "endpoints":
        from sites.fnac.endpoints import CHECKLIST

        for ep in CHECKLIST:
            print(f"{ep.confidence:14} {ep.method:6} [{ep.host}] {ep.path} — {ep.about}")
        return 0

    store = CookieStore(base_path=args.cookies_dir)

    if args.cmd == "analyze-capture":
        from sites.fnac.capture_tools import analyze_capture, load_capture_file

        cap_path = Path(args.capture_in)
        if not cap_path.is_file():
            print(f"Missing file: {cap_path}", file=sys.stderr)
            return 1
        rows = load_capture_file(cap_path)
        rep = analyze_capture(rows)
        print(json.dumps(rep, indent=2, ensure_ascii=False))
        return 0

    if args.cmd == "capture":
        from sites.fnac import config as fnac_config
        from sites.fnac.playwright_fnac import run_endpoint_capture

        ua = args.user_agent or fnac_config.DEFAULT_USER_AGENT
        rows = run_endpoint_capture(
            cookie_store=store,
            output_path=Path(args.out),
            user_agent=ua,
            headless=not args.cap_no_headless,
            referer_path=args.referer_path,
            extra_goto_url=args.extra_url or None,
            auto_click_add_to_cart=args.click_add,
            duration_seconds=args.duration,
            settle_seconds=args.settle,
        )
        report_p = Path(args.out).with_suffix(".report.json")
        print(f"Captured {len(rows)} XHR/fetch calls -> {args.out}")
        print(f"Report -> {report_p}")
        return 0

    headless = True
    transport: str = "auto"
    if args.cmd == "add":
        headless = not args.no_headless
        transport = "httpx" if args.httpx_only else "auto"
    elif args.cmd == "watch":
        headless = not args.no_headless

    buyer = FnacBuyer(
        cookie_store=store,
        user_agent=args.user_agent,
        headless=headless,
        transport=transport if args.cmd == "add" else "auto",
    )

    if args.cmd == "add":
        from sites.fnac.response_summary import format_cli_block

        r = buyer.add_to_cart(
            args.product_id,
            quantity=args.quantity,
            referer_path=args.referer_path,
        )
        print(f"HTTP {r.http_status}")
        print(
            format_cli_block(
                r.http_status,
                r.raw_text,
                body=r.body if isinstance(r.body, (dict, list)) else None,
                verbose=args.verbose,
            )
        )
        return 0 if r.ok else 1

    if args.cmd == "probe":
        if getattr(args, "playwright", False):
            pw_buyer = FnacBuyer(
                cookie_store=store,
                user_agent=args.user_agent,
                headless=not getattr(args, "probe_no_headless", False),
            )
            out = pw_buyer.probe_cart_via_playwright(referer_path=args.referer_path)
        else:
            out = buyer.probe_cart_endpoints(referer_path=args.referer_path)
        print(json.dumps(out, indent=2, default=str)[:12_000])
        return 0

    if args.cmd == "watch":
        pid = args.watch_product_id.strip() or None
        cfg = FnacWatchConfig(
            mode=args.mode,
            search_query=args.query,
            product_url=args.url,
            product_id=pid,
            name_hint=args.name_hint,
            price_min_eur=args.price_min,
            price_max_eur=args.price_max,
        )
        mon = FnacMonitor(cfg, cookie_store=store, buyer=buyer)

        def tick(snap) -> None:
            print(
                json.dumps(
                    {
                        "ready": snap.ready_to_buy,
                        "reason": snap.reason,
                        "product_id": snap.product_id,
                        "price_eur": snap.price_eur,
                        "title": snap.matched_title,
                    },
                    default=str,
                )
            )

        if args.dry_run:
            tick(mon.poll_once())
            return 0
        r = mon.run_loop(
            interval_sec=args.interval,
            max_iterations=args.max_tries,
            on_tick=tick,
        )
        if r and r.ok:
            from sites.fnac.response_summary import summarize_fnac_response

            summ = summarize_fnac_response(r.http_status, r.raw_text, body=r.body)
            print("cart_ok", json.dumps(summ, ensure_ascii=False))
            return 0
        print("no_purchase")
        return 1

    return 1


if __name__ == "__main__":
    sys.exit(main())
