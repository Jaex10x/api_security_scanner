
import typer
from .scanner import scan_urls

app = typer.Typer(help="Simple API security scanner")

@app.command()
def scan(urls: list[str] = typer.Argument(..., help="One or more URLs to scan")):
    scan_urls(urls)

def main() -> None:
    
    app()

if __name__ == "__main__":
    main()
