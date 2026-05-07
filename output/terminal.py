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
        profit_style = "bold green" if opp.profit_pct > 0 else "bold red"
        profit_str = f"{opp.profit_pct:+.2f}%"
        table.add_row(
            opp.arb_type.value.upper(),
            " / ".join(opp.exchanges),
            " → ".join(opp.path),
            profit_str,
            f"{opp.volume:.4f}",
            style=profit_style if opp.profit_pct < 0 else None,
        )
    console.print(table)
    buf = StringIO()
    Console(file=buf).print(table)
    return buf.getvalue()


def format_all_opportunities(
    profits: list[Opportunity],
    losses: list[Opportunity],
    max_rows: int = 10
) -> str:
    """Format both profitable and loss opportunities."""
    table = Table(title="Arbitrage Opportunities")
    table.add_column("Type", style="cyan")
    table.add_column("Exchange(s)", style="green")
    table.add_column("Path", style="yellow")
    table.add_column("Profit %", style="bold")
    table.add_column("Volume", style="dim")

    all_opps = profits + losses
    all_opps.sort(key=lambda o: o.profit_pct, reverse=True)

    shown = 0
    for opp in all_opps:
        if shown >= max_rows:
            break
        profit_style = "green" if opp.profit_pct > 0 else "red"
        profit_str = f"{opp.profit_pct:+.2f}%"
        table.add_row(
            opp.arb_type.value.upper(),
            " / ".join(opp.exchanges),
            " → ".join(opp.path),
            profit_str,
            f"{opp.volume:.4f}",
        )
        shown += 1
    console.print(table)

    if losses:
        console.print(f"[red]Loss opportunities: {len(losses)}[/red]")
    if profits:
        console.print(f"[green]Profit opportunities: {len(profits)}[/green]")

    return ""

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
