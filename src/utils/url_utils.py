import datetime
from typing import List

from src.utils.choise_utils import TitleChoice


def create_url(ticker: str = '', start_date: datetime.date = None, end_date: datetime.date = None,
               sh_price_min: float = 0.0, sh_price_max: float = 0.0, insider_name: str = '', insider_title: list = None,
               sale: bool = False, purchase: bool = False) -> str:
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
            raise NotImplementedError("Jeszcze moment, nie wiem jak to zrobić!")
        case [False, False]:
            pass

    title_str = create_insider_title_str(insider_title)

    url = f"http://openinsider.com/screener?s={ticker}&o={insider_name.replace(' ', '+')}&pl={sh_price_min}&ph={sh_price_max}&" \
          f"ll=&lh=&fd={fd_flag}&fdr={date_range}&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp={int(purchase)}&xs={int(sale)}&" \
          f"vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&{title_str}grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&" \
          f"oc2l=&oc2h=&sortcol=0&cnt=100&page=1"
    return url


def create_insider_title_str(titles: List[TitleChoice]) -> str:
    final_string = ''
    for title in titles:
        match title:
            case TitleChoice.officer:
                final_string += 'isofficer=1&'
            case TitleChoice.COB:
                final_string += 'iscob=1&'
            case TitleChoice.CEO:
                final_string += 'isceo=1&'
            case TitleChoice.Pres:
                final_string += 'ispres=1&'
            case TitleChoice.COO:
                final_string += 'iscoo=1&'
            case TitleChoice.CFO:
                final_string += 'iscfo=1&'
            case TitleChoice.GC:
                final_string += 'isgc=1&'
            case TitleChoice.VP:
                final_string += 'isvp=1&'
            case TitleChoice.Director:
                final_string += 'isdirector=1&'
            case TitleChoice.ten_own:
                final_string += 'istenpercent=1&'
            case TitleChoice.other:
                final_string += 'isother=1&'
            case _:
                pass

    return final_string
