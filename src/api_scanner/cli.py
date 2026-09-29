# SPDX-FileCopyrightText: 2024
# SPDX-License-Identifier: MIT
"""Command-line interface for the API security scanner.

Usage example:
    api-scanner https://example.com https://api.example.org

The CLI uses ``typer`` to parse arguments and forwards the URLs to the
scanner functions defined in :pymod:`api_scanner.scanner`.
"""
import typer
from .scanner import scan_urls

app = typer.Typer(help="Simple API security scanner")

@app.command()
def scan(urls: list[str] = typer.Argument(..., help="One or more URLs to scan")):
    """Scan the supplied URLs and display security‑header reports.

    The command forwards the list of URLs to :func:`scan_urls` which
    performs the actual HTTP requests and prints a formatted table for
    each endpoint.
    """
    scan_urls(urls)

def main() -> None:
    """Entry point used by the console script defined in ``pyproject.toml``.
    """
    app()

if __name__ == "__main__":
    main()
