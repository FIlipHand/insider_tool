import sys
import os

import pandas as pd
import typer
from typing import List
from datetime import datetime
from rich.console import Console
from src.visualization.report import TickerReport, PennyStockReport
from src.visualization.terminal_viz import return_table
from src.utils.url_utils import create_url
from src.scrapping.data import get_data
from src.utils.choise_utils import StyleChoice, TitleChoice, SortChoice
from src.utils.data_utils import process_dataset, group_dataset, format_dataset

sys.path.append(os.getcwd())

app = typer.Typer()

__version__ = '0.5.0'
console = Console()


def version_callback(value: bool):
    if value:
        typer.echo(f"Insider Tool app version: {__version__}")
        raise typer.Exit()


@app.callback()
def common(
        ctx: typer.Context,
        version: bool = typer.Option(
            None, '--version', '-v', callback=version_callback),
):
    pass


@app.command()
def get(ticker: List[str] = typer.Option([], '--ticker', '-k', rich_help_panel="General"),
        since: datetime = typer.Option(None, '--from', '-f', formats=['%d-%m-%Y'], show_default=False,
                                       rich_help_panel="Date"),
        to: datetime = typer.Option(None, '--to', '-t', formats=['%d-%m-%Y'], show_default=False,
                                    rich_help_panel="Date"),
        days_ago: str = typer.Option(
            None, '--days-ago', '-d', show_default=False, rich_help_panel="Date"),
        sh_min: float = typer.Option(
            None, show_default=False, rich_help_panel="General"),
        sh_max: float = typer.Option(
            None, show_default=False, rich_help_panel="General"),
        vol_min: int = typer.Option(
            None, show_default=False, rich_help_panel="General"),
        vol_max: int = typer.Option(
            None, show_default=False, rich_help_panel="General"),
        insider_name: str = typer.Option(
            '', show_default=False, rich_help_panel="General"),
        sale: bool = typer.Option(
            False, '--sale', '-s', rich_help_panel="Transaction Filing"),
        purchase: bool = typer.Option(
            False, '--purchase', '-p', rich_help_panel="Transaction Filing"),
        insider_title: List[TitleChoice] = typer.Option([], '--title', case_sensitive=False, show_default=False,
                                                        rich_help_panel="Transaction Filing"),
        group: bool = typer.Option(
            False, '--group', '-g', rich_help_panel="Additional options"),
        save: bool = typer.Option(
            False, '--save', rich_help_panel="Additional options"),
        report: bool = typer.Option(
            False, '--report', rich_help_panel="Additional options"),
        if_print: bool = typer.Option(
            False, '--print', rich_help_panel="Additional options"),
        style: StyleChoice = typer.Argument(StyleChoice.normal, hidden=True),
        sort: SortChoice = typer.Option(None, '--sort', rich_help_panel="Additional options")):
    if not (sale or purchase):
        sale = True
        purchase = True

    # Since typer only supports datetime as option type we have to work around it to use only date
    to = '' if to is None else to.date()
    since = '' if since is None else since.date()
    if bool(to) is True and bool(since) is False:
        console.print('[red]ERROR: Please specify start date if you want to use end date![/red]')
        raise typer.Exit(code=1)
    proc_data = None

    data = pd.DataFrame()
    page_cnt = 1
    new_date = to
    while True:
        url = create_url(ticker=ticker, start_date=since, end_date=new_date, sh_price_min=sh_min, sh_price_max=sh_max,
                         insider_name=insider_name, insider_title=insider_title, sale=sale, purchase=purchase,
                         volume_max=vol_max, volume_min=vol_min, days_ago=days_ago, page_number=page_cnt)
        new_data = get_data(url)
        data = pd.concat([data, new_data])
        # print(page_cnt)
        if len(new_data) != 5000:
            break
        if page_cnt == 9:
            page_cnt = 1
            new_date = datetime.strptime(data.iloc[-1]['Filing Date'].split(' ')[0], '%Y-%m-%d')
            continue

        page_cnt += 1

    if data.empty:
        console.print('[red]ERROR: There is nothing to show. Exiting...[/red]')
        raise typer.Exit(code=1)

    if insider_name != '':
        # data_name = data.name
        data = data.loc[data['Insider Name'] == insider_name]
        # data.name = data_name
    # Check bool flags
    if group:
        if proc_data is None:
            proc_data = process_dataset(data)
        proc_data = group_dataset(proc_data)
        # proc_data.name = "Insider buys"

    if sort:
        if proc_data is None:
            proc_data = process_dataset(data)
        proc_data.sort_values(by=[sort.value], ascending=False, inplace=True)
        # proc_data = format_dataset(proc_data)

    if if_print:
        table = return_table(data if proc_data is None else format_dataset(proc_data), style.value)
        print_flag = True
        if table.row_count >= 200:
            print_flag = typer.confirm(f"There are {table.row_count} rows to print. Are you sure you want to continue?",
                                       default=True)
        if print_flag:
            console.print(table)

    if save:
        if proc_data is None:
            proc_data = process_dataset(data)
        if not os.path.exists('./data'):
            os.mkdir('./data')
        try:
            name = '_'.join([ticker, since, to])
        except TypeError:
            name = 'data_' + datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
        proc_data.to_csv(f'./data/{name}.csv', index=False)

    if report:
        if not ticker:
            console.print('[red]ERROR: No ticker specified! [/red]')
            raise typer.Exit(code=1)
        elif len(ticker) == 1:
            rp = TickerReport(data)
        else:
            rp = PennyStockReport(data)
            rp.filename = rp.filename.replace('Penny_stocks', '_'.join(ticker))
        try:
            rp.generate_report()
        except AttributeError:
            console.print('[red]ERROR: There is nothing to show. Exiting...[/red]')
            raise typer.Exit(code=1)


@app.command()
def penny_stocks(days_ago: str = typer.Option(None, '--days-ago', '-d', show_default=False, rich_help_panel="Date"),
                 report: bool = typer.Option(
                     False, '--report', rich_help_panel="Additional options"), save: bool = False,
                 group: bool = typer.Option(
                     False, '--group', '-g', rich_help_panel="Additional options"),
                 if_print: bool = typer.Option(
                     False, '--print', rich_help_panel="Additional options"),
                 style: StyleChoice = typer.Argument(StyleChoice.normal, hidden=True),
                 sort: SortChoice = typer.Option(None, '--sort', rich_help_panel="Additional options")):
    url = create_url(sh_price_max=5, volume_min=25_000,
                     purchase=True, days_ago=days_ago)
    data = get_data(url=url)
    # data.name = 'Latest penny stock buys'
    proc_data = None

    if group:
        if proc_data is None:
            proc_data = process_dataset(data)
        proc_data = group_dataset(proc_data)
        # proc_data.name = data.name
    if sort:
        if proc_data is None:
            proc_data = process_dataset(data)
        proc_data.sort_values(by=[sort.value], ascending=False, inplace=True)

    if if_print:
        table = return_table(data if proc_data is None else format_dataset(proc_data), style.value)
        print_flag = True
        if table.row_count >= 200:
            print_flag = typer.confirm(f"There are {table.row_count} rows to print. Are you sure you want to continue?",
                                       default=True)
        if print_flag:
            console.print(table)

    if report:
        rp = PennyStockReport(dataset=data)
        try:
            rp.generate_report()
        except AttributeError:
            console.print('[red]ERROR: There is nothing to show. Exiting...[/red]')
            raise typer.Exit(code=1)
    if save:
        proc_data = process_dataset(data) if proc_data is None else proc_data
        if not os.path.exists('./data'):
            os.mkdir('./data')
        proc_data.to_csv(
            f'./data/penny_stocks_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv', index=False)


@app.command()
def set_up_telegram(ticker: List[str] = typer.Option([], '--ticker', rich_help_panel="General"),
                    sh_min: float = typer.Option(
                        None, show_default=False, rich_help_panel="General"),
                    sh_max: float = typer.Option(
                        None, show_default=False, rich_help_panel="General"),
                    vol_min: int = typer.Option(
                        None, show_default=False, rich_help_panel="General"),
                    vol_max: int = typer.Option(
                        None, show_default=False, rich_help_panel="General"),
                    sale: bool = typer.Option(
                        False, '--sale', '-s', rich_help_panel="Transaction Filing"),
                    purchase: bool = typer.Option(
                        False, '--purchase', '-p', rich_help_panel="Transaction Filing"),
                    insider_title: List[TitleChoice] = typer.Option([], '--title', case_sensitive=False,
                                                                    show_default=False,
                                                                    rich_help_panel="Transaction Filing")):
    from src.telegram_bot.telegram_bot import refresh_and_notify

    url = create_url(ticker=ticker, sh_price_max=sh_max, sh_price_min=sh_min, volume_min=vol_min, volume_max=vol_max,
                     sale=sale, purchase=purchase, insider_title=insider_title, days_ago='1')
    refresh_and_notify(url)


if __name__ == '__main__':
    app()
