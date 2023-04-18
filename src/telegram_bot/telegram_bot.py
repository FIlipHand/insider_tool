import os
import pickle
import time

import pandas as pd
import schedule
import telegram
from dotenv import load_dotenv

from src.scrapping.data import get_data
from src.utils.data_utils import get_data_for_prediction

load_dotenv('.env')
API_KEY = os.getenv("API_KEY")
CHAT_ID = os.getenv("CHAT_ID")


class InsiderBot(telegram.Bot):

    def __init__(self):
        super().__init__(API_KEY)
        self.last_day = None
        with open('models/xgmodel.h5', 'rb') as infile:
            self.prediction_model = pickle.load(infile)

    def send_data(self, url):
        dataframe = get_data(url)
        if dataframe.empty:
            return
        if self.last_day is None:
            self.last_day = pd.DataFrame(columns=dataframe.columns)
            return
        new_rows = pd.merge(dataframe, self.last_day, indicator=True, how='outer') \
            .query('_merge=="left_only"').drop('_merge', axis=1)
        self.last_day = dataframe.copy(deep=True)
        if not new_rows.empty:
            for idx, row in new_rows.iterrows():
                message = f"{row['Ticker']}\n On the {row['Trade Date']} {row['Title']} {row['Insider Name']} " \
                          f"{'sold' if row['Trade Type'].startswith('S') else 'purchased'} " \
                          f" {row['Qty']} shares at the price of {row['Price']} ({row['Value']} in sum)"
                for_model, status = get_data_for_prediction(row)
                if status:
                    predicted_movement = self.prediction_model.predict(for_model.values.reshape(1, -1))
                    bonus_message = f"\nPredicted movement {predicted_movement[0]:.2f}%"
                    message += bonus_message
                self.send_message(CHAT_ID, message)
                time.sleep(1)

    def refresh_and_notify(self, url: str):
        schedule.every(20).seconds.do(lambda: self.send_data(url))
        while True:
            schedule.run_pending()
            time.sleep(1)
