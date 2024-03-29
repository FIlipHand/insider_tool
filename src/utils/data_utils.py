import pandas as pd


def change_cell_to_number(value: str) -> int:
    """
    Parse str value to int
    Examples: "$4,000" -> 4000, "$-12" -> -12
    Parameters
    ----------
    value: str

    Returns
    -------
    int: parsed value
    """
    return int(value.replace('$', '').replace(',', '')) # więcej docstringa niż kodu


def process_dataset(dataset: pd.DataFrame):
    """
    Function takes dataset as argument, then it parses str values to datetime, float or int
    Parameters
    ----------
    dataset: pd.DataFrame

    Returns
    -------
    pd.DataFrame: Dataframe with changed types

    """
    columns = dataset.columns
    if 'Filing Data' in columns:
        dataset['Filing Date'] = pd.to_datetime(dataset['Filing Date'], format="%Y-%m-%d %H:%M:%S")
    if 'Trade Date' in columns:
        dataset['Trade Date'] = pd.to_datetime(dataset['Trade Date'], format="%Y-%m-%d")
    if 'Price' in columns:
        dataset['Price'] = dataset.apply(lambda row: float(row['Price'][1:].replace(',', '')), axis=1)
    if 'Qty' in columns:
        dataset['Qty'] = dataset.apply(lambda row: change_cell_to_number(row['Qty']), axis=1)
    if 'Owned' in columns:
        dataset['Owned'] = dataset.apply(lambda row: change_cell_to_number(row['Owned']), axis=1)
    if 'Value' in columns:
        dataset['Value'] = dataset.apply(lambda row: change_cell_to_number(row['Value']), axis=1)
    return dataset


def group_dataset(dataset: pd.DataFrame):
    """
    Group data by Ticker and Trade Type, then aggregate other columns
    Parameters
    ----------
    dataset: pd.DataFrame to be grouped
    Returns
    -------
    pd.DataFrame: grouped dataframe
    """
    dataset = dataset[['Ticker', 'Trade Type', 'Price', 'Qty', 'Value']]
    dataset = dataset.groupby(by=['Ticker', 'Trade Type']).agg({'Ticker': 'first',
                                                                'Trade Type': 'first',
                                                                'Price': 'mean',  # na pewno? nie powinniśmy tego liczyć jako Value/Qty już po zsumowaniu?
                                                                'Qty': 'sum',
                                                                'Value': 'sum'})
    return dataset


def format_dataset(dataset: pd.DataFrame):
    """
    Reverse of process_dataset() - parse number values back to str
    Parameters
    ----------
    dataset

    Returns
    -------

    """
    dataset['Price'] = dataset.apply(lambda row: '${:.2f}'.format(row['Price']), axis=1)
    dataset['Qty'] = dataset.apply(lambda row: '{:,}'.format(row['Qty']), axis=1)
    dataset['Value'] = dataset.apply(
        lambda row: '-${:,}'.format(abs(row['Value'])) if row['Value'] < 0 else '${:,}'.format(row['Value']), axis=1)
    if 'Owned' in list(dataset.columns):
        dataset['Owned'] = dataset.apply(lambda row: '{:,}'.format(row['Owned']), axis=1)

    return dataset


def get_data_for_prediction(row):
    row = process_dataset(row.to_frame().T)
    status = True
    if row.iloc[0]['Price'] == 0.0 or '.' in row.iloc[0]['Ticker'] or 'Sale' in row.iloc[0]['Trade Type']:
        status = False
    row = row[['Price', 'Qty', 'Owned', 'ΔOwn', 'Value']]
    row['ΔOwn'] = row['ΔOwn'].replace('New', '+100%')
    row['ΔOwn'] = row['ΔOwn'].replace('>999%', '+999%')
    row['ΔOwn'] = int(row.iloc[0]['ΔOwn'][:-1])

    return row, status
