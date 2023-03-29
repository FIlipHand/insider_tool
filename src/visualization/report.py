import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import yfinance as yf
import os


class BaseReport:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset
        self.figure = None
        self.filename = 'base_filename.html'

    def generate_report(self):
        raise NotImplementedError()

    def _get_stock_data(self):
        raise NotImplementedError()

    def _save(self):
        if not os.path.exists('./reports'):
            os.mkdir('./reports')
        self.figure.write_html(f'./reports/{self.filename}')


class TickerReport(BaseReport):
    def __init__(self, dataset: pd.DataFrame):
        super().__init__(dataset=dataset)
        self.ticker = self.dataset.iloc[0]['Ticker']
        self.filename = f'{self.ticker}_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.html'

    def _get_stock_data(self):
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
        return history

    def generate_report(self):
        history = self._get_stock_data()

        self.figure = make_subplots(rows=2, cols=1, vertical_spacing=0.1, specs=[[{"type": "Scatter"}],
                                                                                 [{"type": "table"}]])

        self.figure.add_trace(go.Scatter(x=history.index, y=history['Close'], mode='lines', name='Stock Price'), row=1,
                              col=1)

        colors = []
        for idx, row in self.dataset.iterrows():
            color = 'green' if row['Trade Type'].startswith('P') else 'red'
            self.figure.add_shape(go.layout.Shape(type='line'),
                                  xref='x',
                                  yref='y',
                                  x0=row['Trade Date'],
                                  x1=row['Trade Date'],
                                  y0=-10,
                                  y1=history['Close'].max() * 1.2,
                                  line=dict(color=color))
            colors.append(color)

        new_hist = history.reset_index()
        new_hist['Date'] = new_hist['Date'].dt.date.astype(str)
        new_hist.rename(columns={"Date": "Trade Date"}, inplace=True)
        new_hist = pd.merge(self.dataset, new_hist, on='Trade Date', how='inner')
        new_hist['Price'] = new_hist.apply(lambda x: float(x['Price'][1:]), axis=1)

        self.figure.add_trace(go.Scatter(x=new_hist['Trade Date'],
                                         y=new_hist['Price'],
                                         mode='markers',
                                         customdata=new_hist.values.tolist(),
                                         hovertemplate="<br>Trade Date:%{x}<br>Price:%{y:$.2f}<br>Qty:%{customdata[8]}"
                                                       "<br>Value:%{customdata[11]}",
                                         marker={"color": colors},
                                         name='Insider Trades')
                              )

        self.figure.add_trace(go.Table(header=dict(values=list(self.dataset.columns),
                                                   fill_color='paleturquoise',
                                                   align='left'),
                                       cells=dict(
                                           values=[self.dataset[col_name].to_list() for col_name in
                                                   self.dataset.columns],
                                           fill_color='lavender',
                                           align='left')
                                       ), row=2, col=1)
        self._save()


class PennyStockReport(BaseReport):
    def __init__(self, dataset: pd.DataFrame):
        super().__init__(dataset)
        self.filename = f'Penny_stocks_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.html'
        self.tickers = []

    def _get_stock_data(self):
        self.tickers = self.dataset[['Ticker', 'Trade Date']].groupby(by='Ticker', axis=0).count().index
        ticker_dataframe = pd.DataFrame(columns=self.tickers)
        for ticker in self.tickers:
            stock = yf.Ticker(ticker)
            first_date = datetime.datetime.strptime(self.dataset.iloc[-1]['Trade Date'], '%Y-%m-%d')
            first_date -= datetime.timedelta(days=7)
            last_data = datetime.datetime.strptime(self.dataset.iloc[0]['Trade Date'], '%Y-%m-%d')
            last_data += datetime.timedelta(days=7)
            history = stock.history(start=first_date, end=last_data)
            ticker_dataframe[ticker] = history['Close']
        return ticker_dataframe

    def generate_report(self):
        history = self._get_stock_data()
        self.figure = make_subplots(rows=1, cols=1, vertical_spacing=0.1, specs=[[{"type": "Scatter"}]])
        for i in history.columns:
            self.figure.add_trace(go.Scatter(x=history.index, y=history[i], mode='lines', name=i, legendgroup=i),
                                  row=1, col=1)

        self.dataset['Price'] = self.dataset.apply(lambda x: float(x['Price'][1:]), axis=1)

        for i in self.tickers:
            tmp_data = self.dataset.loc[self.dataset['Ticker'] == i]
            # colors = tmp_data.apply(lambda row: 'red' if row['Trade Type'].startswith('S') else 'green',
            #                         axis=1).values.tolist()
            self.figure.add_trace(go.Scatter(x=tmp_data['Trade Date'],
                                             y=tmp_data['Price'],
                                             mode='markers',
                                             customdata=tmp_data.values.tolist(),
                                             hovertemplate="<br>Trade Date:%{x}<br>Price:%{y:$.2f}<br>"
                                                           "Qty:%{customdata[10]}<br>Value:%{customdata[12]}",
                                             name='Insider Trades',
                                             legendgroup=i,
                                             marker={"color": ['green'] * len(tmp_data.index)}))
        self._save()
