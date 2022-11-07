import datetime

import typer


def create_url(ticker: str = '', start_date: datetime.datetime = None, end_date: datetime.datetime = None,
               sh_price_min: float = 0.0, sh_price_max: float = 0.0, insider_name: str = '', sale: bool = False,
               purchase: bool = False) -> str:
    if sh_price_max == 0.0:
        sh_price_max = ''
    if sh_price_min == 0.0:
        sh_price_min = ''

    fd_flag = 0
    date_range = ''

    match [bool(start_date), bool(end_date)]:
        case [True, True]:
            fd_flag = -1
            date_range = f'{start_date.day}%2F{start_date.month}%2F{start_date.year}+-+' \
                         f'{end_date.day}%2F{end_date.month}%2F{end_date.year}'
        case [True, False]:
            fd_flag = -1
            today = datetime.datetime.now().date()
            date_range = f'{start_date.day}%2F{start_date.month}%2F{start_date.year}+-+' \
                         f'{today.day}%2F{today.month}%2F{today.year}'
        case [False, True]:
            raise NotImplementedError("Jeszcze moment nie wiem jak to zrobić!")
        case [False, False]:
            raise typer.Exit()

    url = f"http://openinsider.com/screener?s={ticker}&o={insider_name.replace(' ', '+')}&pl={sh_price_min}&ph={sh_price_max}&" \
          f"ll=&lh=&fd={fd_flag}&fdr={date_range}&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp={int(purchase)}&xs={int(sale)}&" \
          f"vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1"
    return url
