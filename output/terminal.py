from rich.console import Console
from rich.table import Table
from rich.text import Text
from io import StringIO
from core.models import Opportunity, PaperPortfolio

console = Console()


def format_opportunities(opps: list[Opportunity], max_rows: int = 10) -> str:
    if not opps:
        console.print("[yellow]No opportunities found[/yellow]")
        return ""

    table = Table(title=" Arbitrage Opportunities ", box=None, pad_edge=False)
    table.add_column("TYPE", style="cyan bold", width=14)
    table.add_column("ROUTE", style="white", width=30)
    table.add_column("PROFIT", justify="right", width=10)
    table.add_column("VOL", justify="right", width=8)

    for opp in opps[:max_rows]:
        profit_color = "green" if opp.profit_pct > 0 else "red"
        profit_text = f"+{opp.profit_pct:.4f}%" if opp.profit_pct > 0 else f"{opp.profit_pct:.4f}%"
        
        route = f"{opp.exchanges[0]} [{opp.path[0]}]"
        
        table.add_row(
            opp.arb_type.value.upper(),
            route,
            Text(profit_text, style=f"bold {profit_color}"),
            f"{opp.volume:.2f}",
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


def generate_advice(opps: list[Opportunity], config: dict = None) -> str:
    """Generate AI-like advice based on current opportunities."""
    if not opps:
        console.print("\n[dim]");
        console.print("═" * 60)
        console.print(" AI ANALYSIS");
        console.print("═" * 60);
        console.print("[yellow]No opportunities found.[/yellow]");
        console.print("");
        console.print("This could mean:");
        console.print("  • Markets are efficient right now");
        console.print("  • Too few exchanges returning data");  
        console.print("  • Fees are too high relative to spreads");
        console.print("");
        console.print("Try:");
        console.print("  • Enable more exchanges in config.yaml");
        console.print("  • Lower min_profit_pct in config.yaml");
        console.print("  • Use maker fees (0.01%)");
        console.print("[/dim]\n");
        return ""

    profits = [o for o in opps if o.profit_pct > 0]
    losses = [o for o in opps if o.profit_pct <= 0]
    
    console.print("\n");
    console.print("═" * 60);
    console.print(" AI MARKET ANALYSIS");
    console.print("═" * 60);
    
    if profits:
        best = max(profits, key=lambda o: o.profit_pct)
        console.print(f"[green]✓ Found {len(profits)} profitable opportunity(s)[/green]");
        console.print(f"  Best: {best.arb_type.value} {best.path} = +{best.profit_pct:.4f}%");
        console.print("");
        console.print(" RECOMMENDATION:");
        
        if best.arb_type.value == "cross_exchange":
            console.print(f"  → Buy {best.path[0]} on {best.exchanges[0]}");
            console.print(f"  → Sell on {best.exchanges[1] if len(best.exchanges) > 1 else best.exchanges[0]}");
            console.print(f"  → Expected profit: {best.profit_pct:.4f}% per trade");
        elif best.arb_type.value == "bellman_ford":
            console.print(f"  → Multi-hop cycle detected");
            console.print(f"  → Route: {' → '.join(best.path)}");
            console.print(f"  → Expected profit: {best.profit_pct:.4f}% per cycle");
        elif best.arb_type.value == "triangular":
            console.print(f"  → Execute triangular arbitrage");
            console.print(f"  → Route: {' → '.join(best.path)}");
        else:
            console.print(f"  → Execute {best.arb_type.value} arb");
    else:
        console.print(f"[red]✗ {len(opps)} opportunity(s) found but all negative[/red]");
        
    if losses:
        console.print("");
        console.print(f"[dim]Note: {len(losses)} opportunities have negative profit.[/dim]");
        console.print("[dim]This often means: spreads < fees. Try lower fees or wait for volatility.[/dim]");
    
    console.print("");
    return ""

def clear_screen():
    console.clear()
