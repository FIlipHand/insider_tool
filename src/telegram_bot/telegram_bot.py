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
last_row = ''


def send_data(row):
    global last_row
    if last_row != row.to_string():
        last_row = row.to_string()
        message = f"{row.iloc[0]['Title']} {row.iloc[0]['Insider Name']} {row.iloc[0]['Trade Type']} " \
                  f"on the {row.iloc[0]['Trade Date']} {row.iloc[0]['Qty']} {row.iloc[0]['Ticker']} " \
                  f"shares at the price of {row.iloc[0]['Price']} ({row.iloc[0]['Value']} in sum)"
        bot.send_message(CHAT_ID, message)


def refresh_and_notify(url: str):
    data = get_data(url)
    schedule.every(5).minutes.do(lambda: send_data(data))
    while True:
        schedule.run_pending()
        time.sleep(1)
