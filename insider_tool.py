import sys
import os
import typer
from datetime import datetime
from rich.console import Console
from src.visualization.terminal_viz import return_table
from src.utils.url_utils import create_url
from src.scrapping.data import get_data
from src.utils.choise_utils import StyleChoice

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
def get_ticker(ticker: str, since: datetime = typer.Option(None, '--from', '-f', formats=['%d-%m-%Y']),
               to: datetime = typer.Option(None, '--to', '-t', formats=['%d-%m-%Y']),
               sh_min: float = 0.0, sh_max: float = 0.0,
               insider_name: str = '', sale: bool = typer.Option(False, '--sale', '-s'),
               purchase: bool = typer.Option(False, '--purchase', '-p'), style: StyleChoice = StyleChoice.normal,
               save: bool = typer.Option(False, '--save')):
    if not (sale or purchase):
        raise ValueError('Please specify at least one option with --sale or --purchase')
    url = create_url(ticker=ticker, start_date=since, end_date=to, sh_price_min=sh_min, sh_price_max=sh_max,
                     insider_name=insider_name, sale=sale, purchase=purchase)
    data = get_data(url)
    # to można jakoś inaczej ogarnąć bo na razie syf jest troche
    if insider_name != '':
        data_name = data.name
        data = data.loc[data['Insider Name'] == insider_name]
        data.name = data_name
    table = return_table(data, style.value)
    if table.row_count >= 200:
        print_flag = typer.confirm(f"There are {table.row_count} rows to print. Are you sure you want to continue?",
                                   default=True)
        if print_flag:
            console.print(table)
    else:
        console.print(table)
    if save:
        data.to_csv(f'./data/{ticker}_{since}_{to}.csv', index=False)


@app.command()
def penny_stock(style: str = 'normal'):
    url = 'http://openinsider.com/latest-penny-stock-buys'
    data = get_data(url=url)
    data.name = 'Latest penny stock buys'
    console.print(return_table(data, style))


@app.command()
def cluster_buys(style: str = 'normal'):
    url = 'http://openinsider.com/latest-cluster-buys'
    # TODO tutaj są inne nazwy kolumn więc jakiś handling trzeba ogarnąć
    data = get_data(url=url)
    data.name = 'Latest cluster buys'
    console.print(return_table(data, style))


if __name__ == '__main__':
    app()
