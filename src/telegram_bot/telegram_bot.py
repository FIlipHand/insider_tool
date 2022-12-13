import pandas as pd
import telegram
import os
from dotenv import load_dotenv
import time
import schedule

from src.scrapping.data import get_data

load_dotenv('.env')
API_KEY = os.getenv("API_KEY")
CHAT_ID = os.getenv("CHAT_ID")

bot = telegram.Bot(API_KEY)
last_day = None


def send_data(url):
    global last_day
    dataframe = get_data(url)
    if last_day is None:
        last_day = pd.DataFrame(columns=dataframe.columns)
        return
    new_rows = pd.merge(dataframe, last_day, indicator=True, how='outer') \
        .query('_merge=="left_only"').drop('_merge', axis=1)
    last_day = dataframe.copy(deep=True)
    if not new_rows.empty:
        for idx, row in new_rows.iterrows():
            message = f"{row['Ticker']}\n On the {row['Trade Date']} {row['Title']} {row['Insider Name']} " \
                      f"{'sold' if row['Trade Type'].startswith('S') else 'purchased'} " \
                      f" {row['Qty']} shares at the price of {row['Price']} ({row['Value']} in sum)"
            bot.send_message(CHAT_ID, message)
            time.sleep(1)


def refresh_and_notify(url: str):
    schedule.every(5).minutes.do(lambda: send_data(url))
    while True:
        schedule.run_pending()
        time.sleep(1)
