import pandas as pd


def change_cell_to_number(value: str) -> int:
    value = value.replace('$', '')
    value = value.replace(',', '')
    if value[0] == '-':
        value = value.replace('-', '')
        value = int(value) * -1
    else:
        value = value.replace('+', '')
        value = int(value)
    return value


def process_dataset(dataset: pd.DataFrame):
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
    dataset = dataset[['Ticker', 'Company Name', 'Trade Type', 'Price', 'Qty', 'Value']]
    dataset = dataset.groupby(by=['Ticker', 'Trade Type']).agg({'Company Name': 'first',
                                                                'Ticker': 'first',
                                                                'Trade Type': 'first',
                                                                'Price': 'mean',
                                                                'Qty': 'sum',
                                                                'Value': 'sum'})
    dataset['Price'] = dataset.apply(lambda row: '${:.2f}'.format(row['Price']), axis=1)
    dataset['Qty'] = dataset.apply(lambda row: '{:,}'.format(row['Qty']), axis=1)
    dataset['Value'] = dataset.apply(
        lambda row: '-${:,}'.format(abs(row['Value'])) if row['Value'] < 0 else '${:,}'.format(row['Value']), axis=1)
    return dataset
