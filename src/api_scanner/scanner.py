# SPDX-FileCopyrightText: 2024
# SPDX-License-Identifier: MIT
"""Core scanning functionality for API security.

This module provides a simple scanner that performs HTTP requests
against the supplied endpoint(s) and reports on common security
headers and authentication mechanisms.
"""
import httpx
from rich.console import Console
from rich.table import Table
from typing import List, Tuple

console = Console()

SECURITY_HEADERS = [
    "content-security-policy",
    "strict-transport-security",
    "x-content-type-options",
    "x-frame-options",
    "x-xss-protection",
    "referrer-policy",
    "permissions-policy",
]

def _check_headers(response: httpx.Response) -> List[Tuple[str, str, bool]]:
    """Return a list of tuples (header, value, present)."""
    results = []
    for hdr in SECURITY_HEADERS:
        val = response.headers.get(hdr)
        results.append((hdr, val or "-", bool(val)))
    return results

def scan_url(url: str) -> None:
    """Fetch *url* and display a security‑header report.

    The function performs a simple GET request (following redirects) and
    prints a table indicating which of the common security headers are
    present. It also reports the HTTP status code and the final URL after
    redirects.
    """
    try:
        resp = httpx.get(url, follow_redirects=True, timeout=10.0)
    except Exception as exc:
        console.print(f"[red]Failed to fetch {url}: {exc}[/red]")
        return

    table = Table(title=f"Security Header Report for {url}")
    table.add_column("Header", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    table.add_column("Present", style="green")

    for hdr, val, present in _check_headers(resp):
        table.add_row(hdr, val, "✅" if present else "❌")

    console.print(f"[bold]Status:[/bold] {resp.status_code}  [bold]Final URL:[/bold] {resp.url}")
    console.print(table)

def scan_urls(urls: List[str]) -> None:
    """Scan a list of URLs sequentially."""
    for u in urls:
        scan_url(u)

__all__ = ["scan_url", "scan_urls"]
