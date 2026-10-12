""" Risk based investment allocator
This Project uses sample allocations
"""

from dataclasses import dataclass

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, FloatPrompt, Prompt
from rich.table import Table
from rich.text import Text


console = Console()


@dataclass(frozen=True)
class Investment:
    """One sample investment in an allocation plan."""

    ticker: str
    name: str
    percentage: int
    price: float


PLANS: dict[str, dict[str, object]] = {
    "Conservative": {
        "reason": (
            "This example puts more weight in bonds and broad diversification "
            "to match a lower-risk preference."
        ),
        "investments": [
            Investment("BND", "Bond ETF", 40, 73.00),
            Investment("VOO", "S&P 500 ETF", 30, 540.00),
            Investment("JNJ", "Healthcare stock", 15, 165.00),
            Investment("KO", "Consumer staples stock", 15, 70.00),
        ],
    },
    "Moderate": {
        "reason": (
            "This example balances a diversified ETF foundation with some "
            "growth exposure."
        ),
        "investments": [
            Investment("VOO", "S&P 500 ETF", 40, 540.00),
            Investment("MSFT", "Large-company stock", 20, 480.00),
            Investment("AAPL", "Consumer technology stock", 15, 250.00),
            Investment("JNJ", "Healthcare stock", 15, 165.00),
            Investment("NVDA", "Growth stock", 10, 190.00),
        ],
    },
    "Aggressive": {
        "reason": (
            "This example gives more weight to growth investments, which can "
            "also mean more volatility."
        ),
        "investments": [
            Investment("QQQ", "Growth-focused ETF", 35, 610.00),
            Investment("NVDA", "Growth stock", 25, 190.00),
            Investment("AMZN", "Growth stock", 20, 220.00),
            Investment("TSLA", "Electric-vehicle growth stock", 10, 350.00),
            Investment("PLTR", "Software growth stock", 10, 180.00),
        ],
    },
}

def format_money(amount: float) -> str:
    """Return a dollar amount with commas and two decimal places."""
    return f"${amount:,.2f}"


def choose_risk_tolerance() -> str:
    """Ask until the user chooses a valid risk tolerance."""
    choices = {"1": "Conservative", "2": "Moderate", "3": "Aggressive"}

    console.print("\n[bold]Choose your risk tolerance:[/bold]")
    console.print("  [cyan]1.[/cyan] Conservative")
    console.print("  [cyan]2.[/cyan] Moderate")
    console.print("  [cyan]3.[/cyan] Aggressive")

    while True:
        choice = Prompt.ask("Your choice", choices=list(choices))
        if choice in choices:
            return choices[choice]


def show_allocation(amount: float, risk_level: str) -> None:
    """Display a styled allocation table for the selected plan."""
    plan = PLANS[risk_level]
    investments = plan["investments"]

    title = Text(f"{risk_level} allocation for {format_money(amount)}", style="bold green")
    table = Table(title=title, title_justify="left", header_style="bold #19D39A", border_style="#2A2A31",)
    table.add_column("Investment", style="bold")
    table.add_column("Description")
    table.add_column("Allocation", justify="right")
    table.add_column("Budget", justify="right")
    table.add_column("Mock Price", justify="right")
    table.add_column("Whole Shares", justify="right", style="bold #19D39A")
    table.add_column("Leftover", justify="right")

    for investment in investments:
        investment_amount = amount * investment.percentage / 100
        whole_shares = int(investment_amount // investment.price)
        money_used = whole_shares * investment.price
        leftover_cash = investment_amount - money_used
        table.add_row(
            investment.ticker,
            investment.name,
            f"{investment.percentage}%",
            format_money(investment_amount),
            format_money(investment.price),
            str(whole_shares),
            format_money(leftover_cash),
        )

    console.print()
    console.print(table)
    console.print(
        Panel(
            str(plan["reason"]),
            title="Why this plan?",
            border_style="#E92B35",
            style="on #151519",
        )
    )


def run_allocator() -> None:
    """Run one allocation interaction."""
    console.print(
        Panel(
            Align.center(
                "[bold bright_green]Strata Risk Allocator[/bold bright_green]\n"
                "[dim]Enter an amount and choose your investment risk level[/dim]"
            ),
            border_style="#E92B35",
            style ="on #151519",
        )
    )

    amount = FloatPrompt.ask(
        "\nHow much would you like to invest?",
        default=1000.0,
    )
    while amount <= 0:
        console.print("[red]Please enter an amount greater than $0.[/red]")
        amount = FloatPrompt.ask("How much would you like to invest?")

    risk_level = choose_risk_tolerance()
    show_allocation(amount, risk_level)


def main() -> None:
    """Keep the program open until the user chooses to exit."""
    while True:
        console.clear()
        run_allocator()
        if not Confirm.ask("\nCreate another allocation?", default=True):
            console.print("\n[bold green]Thanks for trying Strata![/bold green]")
            break


if __name__ == "__main__":
    main()
