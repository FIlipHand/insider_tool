def get_colored_text(text, color: str) -> str:
    assert color in {'red', 'green', 'yellow'}
    return "[{0}]{1}[/{0}]".format(color, text)


def color_row(row):
    if row['Trade Type'].startswith('P'):
        color = 'green'
    elif row['Trade Type'].endswith('OE'):
        color = 'yellow'
    else:
        color = 'red'
    for key in 'Value', 'Qty', 'Trade Type':
        row[key] = get_colored_text(row[key], color)
    return row
