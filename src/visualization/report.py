import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import yfinance as yf


class DataReport:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset
        self.ticker = self.dataset.iloc[0]['Ticker']

    def __get_stock_data(self):
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
        history = self.__get_stock_data()

        fig = make_subplots(rows=2, cols=1, vertical_spacing=0.1, specs=[[{"type": "Scatter"}],
                                                                         [{"type": "table"}]])

        fig.add_trace(go.Scatter(x=history.index, y=history['Close'], mode='lines', name='Stock Price'), row=1, col=1)

        colors = []
        for idx, row in self.dataset.iterrows():
            if row['Trade Type'].startswith('P'):
                color = 'green'
            else:
                color = 'red'
            fig.add_shape(go.layout.Shape(type='line'),
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

        fig.add_trace(go.Scatter(x=new_hist['Trade Date'],
                                 y=new_hist['Price'],
                                 mode='markers',
                                 customdata=new_hist.values.tolist(),
                                 hovertemplate="<br>Trade Date:%{x}<br>Price:%{y:$.2f}<br>Qty:%{customdata[8]}"
                                               "<br>Value:%{customdata[11]}",
                                 marker={"color": colors},
                                 name='Insider Trades')
                      )

        fig.add_trace(go.Table(header=dict(values=list(self.dataset.columns),
                                           fill_color='paleturquoise',
                                           align='left'),
                               cells=dict(
                                   values=[self.dataset[col_name].to_list() for col_name in self.dataset.columns],
                                   fill_color='lavender',
                                   align='left')
                               ), row=2, col=1)
        fig.show()
