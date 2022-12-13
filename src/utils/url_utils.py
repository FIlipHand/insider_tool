import datetime
from typing import List

from src.utils.choise_utils import TitleChoice


def create_url(ticker: str = '', start_date: datetime.date = None, end_date: datetime.date = None,
               sh_price_min: float = None, sh_price_max: float = None, insider_name: str = '',
               insider_title: list = None, sale: bool = False, purchase: bool = False, volume_min: int = None,
               volume_max: int = None, days_ago: str = None, n: int = 1000) -> str:
    # it is probably not most elegant way of doing it, but if argument is None we have to change it to empty string
    # in order to properly insert it into final link
    if sh_price_max is None:
        sh_price_max = ''
    if sh_price_min is None:
        sh_price_min = ''
    if days_ago is None:
        days_ago = ''
    if days_ago.isnumeric():
        days_ago = int(days_ago)
    elif len(days_ago) >= 2:
        units = {'d': 1, 'w': 7, 'm': 30, 'y': 365}
        unit = days_ago[-1]
        days_ago = int(days_ago[:-1]) * units[unit.lower()]

    volume_min = '' if volume_min is None else int(volume_min / 1000)
    volume_max = '' if volume_max is None else int(volume_max / 1000)
    insider_title = [] if insider_title is None else insider_title

    # Process dates
    fd_flag = days_ago
    date_range = ''

    match [bool(start_date), bool(end_date)]:
        case [True, True]:
            fd_flag = -1
            date_range = f'{start_date.month}%2F{start_date.day}%2F{start_date.year}+-+' \
                         f'{end_date.month}%2F{end_date.day}%2F{end_date.year}'
        case [True, False]:
            fd_flag = -1
            today = datetime.datetime.now().date()
            date_range = f'{start_date.month}%2F{start_date.day}%2F{start_date.year}+-+' \
                         f'{today.month}%2F{today.day}%2F{today.year}'
        case [False, True]:
            raise NotImplementedError("Jeszcze moment!")
        case [False, False]:
            pass

    # Process insider titles
    title_str = create_insider_title_str(insider_title)

    # TODO jakoś trzeba ogarnąć ilość akcji pobieranych
    url = f"http://openinsider.com/screener?s={ticker}&o={insider_name.replace(' ', '+')}&pl={sh_price_min}&ph={sh_price_max}&" \
          f"ll=&lh=&fd={fd_flag}&fdr={date_range}&td=&tdr=&fdlyl=&fdlyh=&daysago=&xp={int(purchase)}&xs={int(sale)}&" \
          f"vl={volume_min}&vh={volume_max}&ocl=&och=&sic1=-1&sicl=100&sich=9999&{title_str}grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt={n}&page=1"
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
