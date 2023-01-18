# Python tool for Open Insider

```
                        _           _     _
  ___  _ __   ___ _ __ (_)_ __  ___(_) __| | ___ _ __ _ __  _   _
 / _ \| '_ \ / _ \ '_ \| | '_ \/ __| |/ _` |/ _ \ '__| '_ \| | | |
| (_) | |_) |  __/ | | | | | | \__ \ | (_| |  __/ |_ | |_) | |_| |
 \___/| .__/ \___|_| |_|_|_| |_|___/_|\__,_|\___|_(_)| .__/ \__, |
      |_|                                            |_|    |___/
```

## Examples

- Print table containing all insider trades from 01-01-2021 to 01-02-2022 (bad idea)

    - `python insider_tool.py get -f 01-01-2021 -t 01-02-2022 --print `

- Print grouped table with all sales from last month

    - `python insider_tool.py get -s --days-ago 1m -g --print`

- Generate report for all JP Morgan insider trades form this year

    - `python insider_tool.py get --ticker JPM --from 01-01-2022 --report`

- Print short table with all Tesla purchases with share price above $100
    - `python insider_tool.py get --ticker TSLA -p --sh-min 100 --print short`

- Generate report with penny stock bought from last 5 days
    - `python insider_tool.py penny-stocks --days-ago 5d --report`

- Save Lockheed Martin's insider trades from a year to a file for later analysis
    - `python .\insider_tool.py get --ticker LMT -d 1y --save`

- Show Elon Musk's insider traders over with value over $10M
  - `python .\insider_tool.py get --days-ago 1m --insider-name "Musk Elon" --vol-min 10000000 --print`
