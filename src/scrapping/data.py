from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

from src.utils.color_utils import get_colored_text
from src.utils.url_utils import create_url
from src.visualization.terminal_viz import show_dataframe


def get_data(url: str) -> pd.DataFrame:
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

    # r = requests.get(url=url, headers=headers)

    with open('out.html', 'r') as f:
        out = f.read()

    soup = bs(out, "html5lib")
    table = soup.find("table", {'class': "tinytable"})

    new_columns = [i.text.strip().replace(u'\xa0', u' ') for i in table.thead.find_all('h3')]
    dataframe = pd.DataFrame(columns=new_columns)

    for row in table.find_all('tr'):
        new_row = []
        for col in row.find_all('td'):
            text_only = col.text.strip()
            new_row.append(text_only if text_only != '' else None)
        if new_row:
            new_df = pd.DataFrame([dict(zip(new_columns, new_row))])
            if new_df['Trade Type'][0].startswith('P'):
                new_df['Value'][0] = get_colored_text(new_df['Value'][0], 'green')
                new_df['Qty'][0] = get_colored_text(new_df['Qty'][0], 'green')
                new_df['Trade Type'][0] = get_colored_text(new_df['Trade Type'][0], 'green')
            elif new_df['Trade Type'][0].endswith('OE'):
                new_df['Value'][0] = get_colored_text(new_df['Value'][0], 'yellow')
                new_df['Qty'][0] = get_colored_text(new_df['Qty'][0], 'yellow')
                new_df['Trade Type'][0] = get_colored_text(new_df['Trade Type'][0], 'yellow')
            else:
                new_df['Value'][0] = get_colored_text(new_df['Value'][0], 'red')
                new_df['Qty'][0] = get_colored_text(new_df['Qty'][0], 'red')
                new_df['Trade Type'][0] = get_colored_text(new_df['Trade Type'][0], 'red')
            dataframe = pd.concat([dataframe, new_df], ignore_index=True)

    return dataframe


if __name__ == '__main__':
    print(get_data(create_url('AAPL')).head().to_string())
