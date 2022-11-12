import datetime
import os.path
import plotly.express as px
import pandas as pd
import yfinance as yf
from src.utils.project_utils import get_project_root


class DataReport:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset
        self.ticker = self.dataset.iloc[0]['Ticker']

    def get_stock_data(self):
        first_date = self.dataset.iloc[-1]['Trade Date']
        if isinstance(first_date, str):
            first_date = datetime.datetime.strptime(first_date, '%Y-%m-%d')
        first_date -= datetime.timedelta(days=7)
        last_data = self.dataset.iloc[0]['Trade Date']
        if isinstance(last_data, str):
            last_data = datetime.datetime.strptime(last_data, '%Y-%m-%d')
        last_data += datetime.timedelta(days=7)
        stock = yf.Ticker(self.ticker)
        history = stock.history(start=first_date, end=last_data)
        fig = px.line(history, x=history.index, y='Close', title=f'{self.ticker} stock')
        for idx, row in self.dataset.iterrows():
            if row['Trade Type'].startswith('P'):
                color = 'green'
            else:
                color = 'red'
            fig.add_vline(x=row['Trade Date'], line_color=color)
        fig.show()


# da = pd.read_csv(os.path.join(get_project_root(), 'data/JPM__.csv'))
# report = DataReport(da)
# report.get_stock_data()
