import pandas as pd
from tabulate import tabulate

from src.utils.color_utils import color_row


def show_dataframe(dataframe: pd.DataFrame, table_format: str = 'normal'):
    assert table_format == 'short' or \
           table_format == 'normal' or \
           table_format == 'full'

    dataframe = dataframe.apply(lambda row: color_row(row), axis=1)

    if table_format == 'short':
        dataframe.drop(
            columns=['X', 'Filing Date', 'Ticker', 'Insider Name', 'Title', 'Owned', 'ΔOwn', '1d', '1w', '1m', '6m'],
            inplace=True)
    elif table_format == 'normal':
        dataframe.drop(columns=['X', '1d', '1w', '1m', '6m'], inplace=True)

    print(tabulate(dataframe, headers='keys', tablefmt='rounded_grid'))
