import pandas as pd
from rich.console import Console
from rich.table import Table
from rich import box
from src.utils.color_utils import color_row


def show_dataframe(dataframe: pd.DataFrame, table_format: str):
    assert table_format == 'short' or \
           table_format == 'normal' or \
           table_format == 'full'

    table = Table(title=f'{dataframe.name}', box=box.ROUNDED)
    console = Console()
    if table_format == 'short':
        dataframe.drop(
            columns=['X', 'Filing Date', 'Ticker', 'Insider Name', 'Title', 'Owned', 'ΔOwn', '1d', '1w', '1m', '6m'],
            inplace=True)
    elif table_format == 'normal':
        dataframe.drop(columns=['X', '1d', '1w', '1m', '6m'], inplace=True)

    for column in dataframe.columns:
        table.add_column(column)

    dataframe = dataframe.apply(lambda row: color_row(row), axis=1)
    for row in dataframe.itertuples():
        table.add_row(*[str(i) if i else '---' for i in row][1:])
    console.print(table)
    # print(tabulate(dataframe, headers='keys', tablefmt='rounded_grid'))
