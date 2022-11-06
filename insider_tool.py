import sys
import os
import typer
from src.visualization.terminal_viz import show_dataframe
from src.utils.url_utils import create_url
from src.scrapping.data import get_data

sys.path.append(os.getcwd())

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


@app.command()
def show_table(ticker: str, style: str = 'normal'):
    show_dataframe(get_data(create_url(ticker)), style)


if __name__ == '__main__':
    app()
