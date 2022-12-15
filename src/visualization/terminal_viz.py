import pandas as pd
from rich.table import Table
from rich import box
from src.utils.color_utils import color_row


def return_table(dataframe: pd.DataFrame, table_format):
    # table = Table(title=f'{dataframe.name}', box=box.ROUNDED)
    table = Table(box=box.ROUNDED)

    # ignoring errors during dropping means that if column is absent it will be ignored
    if table_format == 'short':
        new_dataframe = dataframe.drop(
            columns=['X', 'Filing Date', 'Ticker', 'Insider Name', 'Title', 'Owned', 'ΔOwn', '1d', '1w', '1m', '6m'],
            errors='ignore')
    elif table_format == 'normal':
        new_dataframe = dataframe.drop(columns=['X', '1d', '1w', '1m', '6m'], errors='ignore')
    else:
        new_dataframe = dataframe

    for column in new_dataframe.columns:
        table.add_column(column)

    new_dataframe = new_dataframe.apply(lambda row: color_row(row), axis=1)
    for row in new_dataframe.itertuples():
        table.add_row(*[str(i) if i else '---' for i in row][1:])
    return table
