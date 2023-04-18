from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import yfinance as yf


def get_data(url: str) -> pd.DataFrame:
    """
    Function used to parse html table from site to pd.DataFrame
    Parameters
    ----------
    url - Valid URL to openinsider.com

    Returns
    -------
    pd.DataFrame containing data
    """
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

    response = requests.get(url=url, headers=headers)

    soup = bs(response.content, "html5lib")
    table = soup.find("table", {'class': "tinytable"})
    if not table:
        return pd.DataFrame()

    new_columns = [i.text.strip().replace('\xa0', ' ') for i in table.thead.find_all('h3')]  # w Pythonie 3 wszystkie stringi są unicode'owe
    partial_dataframes = [pd.DataFrame(columns=new_columns)]

    for row in table.find_all('tr'):
        new_row = []
        for col in row.find_all('td'):
            text_only = col.text.strip()
            new_row.append(text_only if text_only else None)
        if new_row:
            partial_dataframes += [pd.DataFrame([dict(zip(new_columns, new_row))])]

    # # TODO sprawdzenie czy ten ticker na pewno istnieje
    # ticker_info = yf.Ticker(dataframe.iloc[0]['Ticker'])
    # dataframe.name = f'{ticker_info.info["shortName"]} insider trades.'
    return pd.concat(partial_dataframes, ignore_index=True)
