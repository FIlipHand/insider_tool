def get_colored_text(text, color: str) -> str:
    assert color == 'red' or color == 'green' or color == 'yellow'
    if color == 'red':
        out = '[red]' + str(text) + f'[/red]'
    elif color == 'green':
        out = '[green]' + str(text) + f'[/green]'
    elif color == 'yellow':
        out = '[yellow]' + str(text) + f'[/yellow]'
    else:
        out = str(text)
    return out


def color_row(row):
    if row['Trade Type'].startswith('P'):
        row['Value'] = get_colored_text(row['Value'], 'green')
        row['Qty'] = get_colored_text(row['Qty'], 'green')
        row['Trade Type'] = get_colored_text(row['Trade Type'], 'green')
    elif row['Trade Type'].endswith('OE'):
        row['Value'] = get_colored_text(row['Value'], 'yellow')
        row['Qty'] = get_colored_text(row['Qty'], 'yellow')
        row['Trade Type'] = get_colored_text(row['Trade Type'], 'yellow')
    else:
        row['Value'] = get_colored_text(row['Value'], 'red')
        row['Qty'] = get_colored_text(row['Qty'], 'red')
        row['Trade Type'] = get_colored_text(row['Trade Type'], 'red')
    return row
