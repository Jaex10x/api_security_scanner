import httpx
from rich.console import Console
from rich.table import Table
from typing import List, Tuple
from rich.console import Console
from rich.table import Table

console = Console()
SEVERITY_STYLES = {
    "Critical": "[bold red]Critical[/]",
    "High": "[red]High[/]",
    "Medium": "[yellow]Medium[/]",
    "Low": "[blue]Low[/]",
    "Info": "[magenta]Info[/]",
}


def print_report(findings):
    table = Table(title="Findings")
    table.add_column("Method")
    table.add_column("Risk")
    table.add_column("OWASP")
    table.add_column("Issue")

    for f in findings:
        table.add_row(
            f["method"],
            SEVERITY_STYLES.get(f["severity"], f["severity"]),
            f["owasp"],
            f["issue"],
        )

    console.print(table)

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
