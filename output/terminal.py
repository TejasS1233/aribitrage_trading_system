from rich.console import Console
from rich.table import Table
from io import StringIO
from core.models import Opportunity, PaperPortfolio

console = Console()

def format_opportunities(opps: list[Opportunity], max_rows: int = 10) -> str:
    table = Table(title="Arbitrage Opportunities")
    table.add_column("Type", style="cyan")
    table.add_column("Exchange(s)", style="green")
    table.add_column("Path", style="yellow")
    table.add_column("Profit %", style="bold green")
    table.add_column("Volume", style="dim")

    for opp in opps[:max_rows]:
        table.add_row(
            opp.arb_type.value.upper(),
            " / ".join(opp.exchanges),
            " → ".join(opp.path),
            f"+{opp.profit_pct:.2f}%",
            f"{opp.volume:.4f}",
        )
    console.print(table)
    buf = StringIO()
    Console(file=buf).print(table)
    return buf.getvalue()

def format_portfolio(p: PaperPortfolio) -> str:
    lines = [
        f"Portfolio: ${p.total_value_usd:,.2f}",
        f"Trades: {p.total_trades} | Wins: {p.wins} | Losses: {p.losses}",
        f"Win Rate: {p.wins/p.total_trades*100:.1f}%" if p.total_trades > 0 else "Win Rate: N/A",
        f"Total PnL: ${p.total_pnl:+,.2f}",
    ]
    text = " | ".join(lines)
    console.print(f"\n[bold]{text}[/bold]\n")
    return text

def clear_screen():
    console.clear()
