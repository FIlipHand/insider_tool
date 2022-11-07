import datetime


def create_url(ticker: str, start_date: str = None, end_date: str = None, sh_price_min: float = 0.0,
               sh_price_max: float = 0.0, insider_name: str = '') -> str:
    if sh_price_max == 0.0:
        sh_price_max = ''
    if sh_price_min == 0.0:
        sh_price_min = ''

    fd_flag = 0
    date_range = ''
    if start_date:
        fd_flag = -1
        start_date_dt = datetime.datetime.strptime(start_date, '%d/%m/%Y')
        if end_date:
            end_date_dt = datetime.datetime.strptime(end_date, '%d/%m/%Y')
        else:
            end_date_dt = datetime.datetime.now().date()
        date_range = f'{start_date_dt.day}%2F{start_date_dt.month}%2F{start_date_dt.year}+-+' \
                     f'{end_date_dt.day}%2F{end_date_dt.month}%2F{end_date_dt.year}'
    if end_date:
        fd_flag = -1
        end_date_dt = datetime.datetime.strptime(end_date, '%d/%m/%Y')
        if start_date:
            start_date_dt = datetime.datetime.strptime(start_date, '%d/%m/%Y')
        else:
            # TODO jak jest tylko do jakiejś daty do handling tego
            raise NotImplementedError(":(")
        date_range = f'{start_date_dt.day}%2F{start_date_dt.month}%2F{start_date_dt.year}+-+' \
                     f'{end_date_dt.day}%2F{end_date_dt.month}%2F{end_date_dt.year}'

    url = f"http://openinsider.com/screener?s={ticker}&o={insider_name.replace(' ', '+')}&pl={sh_price_min}&ph={sh_price_max}&" \
          f"ll=&lh=&fd={fd_flag}&fdr={date_range}&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&xs=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1"
    return url
