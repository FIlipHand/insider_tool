import sys
import os
import typer
from src.visualization.terminal_viz import show_dataframe
from src.utils.url_utils import create_url
from src.scrapping.data import get_data

sys.path.append(os.getcwd())

app = typer.Typer()

__version__ = '0.1.0'


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
def get_ticker(ticker: str, since: str = '', to: str = '', sh_min: float = 0, sh_max: float = 0,
               insider_name: str = '', style: str = 'normal', save: bool = False):
    url = create_url(ticker=ticker, start_date=since, end_date=to, sh_price_min=sh_min, sh_price_max=sh_max,
                     insider_name=insider_name)
    data = get_data(url)
    if insider_name != '':
        data_name = data.name
        data = data.loc[data['Insider Name'] == insider_name]
        data.name = data_name
    show_dataframe(data, style)
    if save:
        data.to_csv(f'./data/{ticker}-{since}-{to}.csv', index=False)


def penny_stocks():
    url = 'http://openinsider.com/latest-penny-stock-buys'


if __name__ == '__main__':
    app()
