import sys
import os
import typer
from typing import List, Optional
from datetime import datetime
from rich.console import Console

from src.visualization.report import TickerReport, PennyStockReport
from src.visualization.terminal_viz import return_table
from src.utils.url_utils import create_url
from src.scrapping.data import get_data
from src.utils.choise_utils import StyleChoice, TitleChoice
from src.utils.data_utils import process_dataset, group_dataset

sys.path.append(os.getcwd())

app = typer.Typer()

__version__ = '0.1.0'
console = Console()


def version_callback(value: bool):
    if value:
        typer.echo(f"Insider Tool app version: {__version__}")
        raise typer.Exit()


@app.callback()
def common(
        ctx: typer.Context,
        version: bool = typer.Option(None, "--version", callback=version_callback),
):
    pass


@app.command()
def get(ticker: str = '',
        since: datetime = typer.Option(None, '--from', '-f', formats=['%d-%m-%Y'], show_default=False),
        to: datetime = typer.Option(None, '--to', '-t', formats=['%d-%m-%Y'], show_default=False),
        days_ago: str = typer.Option(None, '--days-ago', '-d', show_default=False),
        sh_min: float = typer.Option(None, show_default=False),
        sh_max: float = typer.Option(None, show_default=False),
        vol_min: int = typer.Option(None, show_default=False),
        vol_max: int = typer.Option(None, show_default=False),
        insider_name: str = typer.Option('', show_default=False),
        sale: bool = typer.Option(False, '--sale', '-s'),
        purchase: bool = typer.Option(False, '--purchase', '-p'),
        insider_title: List[TitleChoice] = typer.Option([], '--title', case_sensitive=False, show_default=False),
        group: bool = typer.Option(False, '--group', '-g'),
        save: bool = typer.Option(False, '--save'),
        report: bool = typer.Option(False, '--report'),
        # TODO it's not perfect but gets the job done
        # alternative -> style: StyleChoice = typer.Option(None, '--print')):
        if_print: bool = typer.Option(False, '--print'),
        style: StyleChoice = typer.Argument(StyleChoice.normal, hidden=True)):
    if not (sale or purchase):
        sale = True
        purchase = True

    # Since typer only supports datetime as option type we have to work around it to use only date
    to = '' if to is None else to.date()
    since = '' if since is None else since.date()
    proc_data = None

    url = create_url(ticker=ticker, start_date=since, end_date=to, sh_price_min=sh_min, sh_price_max=sh_max,
                     insider_name=insider_name, insider_title=insider_title, sale=sale, purchase=purchase,
                     volume_max=vol_max, volume_min=vol_min, days_ago=days_ago)
    data = get_data(url)

    if data.empty:
        console.print('[red]ERROR: There is nothing to show. Exiting...[/red]')
        raise typer.Exit(code=1)

    # to można jakoś inaczej ogarnąć bo na razie syf jest troche
    if insider_name != '':
        data_name = data.name
        data = data.loc[data['Insider Name'] == insider_name]
        data.name = data_name

    # Check bool flags
    if group:
        proc_data = process_dataset(data) if proc_data is None else proc_data
        proc_data = group_dataset(proc_data)
        proc_data.name = "Insider buys"

    if if_print:
        table = return_table(data if proc_data is None else proc_data, style.value)
        print_flag = True
        if table.row_count >= 200:
            print_flag = typer.confirm(f"There are {table.row_count} rows to print. Are you sure you want to continue?",
                                       default=True)
        if print_flag:
            console.print(table)

    if save:
        proc_data = process_dataset(data) if proc_data is None else proc_data
        if not os.path.exists('./data'):
            os.mkdir('./data')
        proc_data.to_csv(f'./data/{ticker}_{since}_{to}.csv', index=False)

    if report:
        rp = TickerReport(data)
        rp.generate_report()


@app.command()
def penny_stock(style: StyleChoice = StyleChoice.normal, days_ago: str = None,
                report: bool = False, save: bool = False, group: bool = False, if_print: bool = True):
    url = create_url(sh_price_max=5, volume_min=25_000, purchase=True, days_ago=days_ago)
    data = get_data(url=url)
    data.name = 'Latest penny stock buys'
    proc_data = None

    if group:
        proc_data = process_dataset(data) if proc_data is None else proc_data
        proc_data = group_dataset(proc_data)
        proc_data.name = data.name

    if if_print:
        console.print(return_table(data if proc_data is None else proc_data, style.value))

    if report:
        rp = PennyStockReport(dataset=data)
        rp.generate_report()
    if save:
        proc_data = process_dataset(data) if proc_data is None else proc_data
        if not os.path.exists('./data'):
            os.mkdir('./data')
        proc_data.to_csv(f'./data/penny_stocks_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv', index=False)


if __name__ == '__main__':
    app()
