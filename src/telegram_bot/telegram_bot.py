import pandas as pd
import telegram
import os
from dotenv import load_dotenv
import time
import schedule
import pickle
from src.scrapping.data import get_data
from src.utils.data_utils import get_data_for_prediction

load_dotenv('.env')
API_KEY = os.getenv("API_KEY")
CHAT_ID = os.getenv("CHAT_ID")

bot = telegram.Bot(API_KEY)
last_day = None
with open('models/xgmodel.h5', 'rb') as file:
    prediction_model = pickle.load(file)


def send_data(url):
    global last_day  # nie da się tego uniknąć?
    dataframe = get_data(url)
    if dataframe.empty:
        return
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
            for_model, status = get_data_for_prediction(row)
            if status:
                predicted_movement = prediction_model.predict(for_model.values.reshape(1, -1))
                bonus_message = f"\nPredicted movement {predicted_movement[0]:.2f}%"
                message += bonus_message
            bot.send_message(CHAT_ID, message)
            time.sleep(1)


def refresh_and_notify(url: str):
    schedule.every(20).seconds.do(lambda: send_data(url))
    while True:
        schedule.run_pending()
        time.sleep(1)
