import pandas as pd
from rich.table import Table
from rich import box
from src.utils.color_utils import color_row


def return_table(dataframe: pd.DataFrame, table_format):
    table = Table(title=f'{dataframe.name}', box=box.ROUNDED)

    if table_format == 'short':
        dataframe.drop(
            columns=['X', 'Filing Date', 'Ticker', 'Insider Name', 'Title', 'Owned', 'ΔOwn', '1d', '1w', '1m', '6m'],
            inplace=True)
    elif table_format == 'normal':
        dataframe.drop(columns=['X', '1d', '1w', '1m', '6m'], inplace=True)

    for column in dataframe.columns:
        table.add_column(column)

    # TODO kolorki będą ogarnięte obiecuje...
    colored_df = dataframe.apply(lambda row: color_row(row), axis=1)
    for row in colored_df.itertuples():
        table.add_row(*[str(i) if i else '---' for i in row][1:])
    return table
