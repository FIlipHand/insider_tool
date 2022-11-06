def get_colored_text(text: str, color: str) -> str:
    assert color == 'red' or color == 'green' or color == 'yellow'
    if color == 'red':
        out = '[red]' + text + f'[/red]'
    elif color == 'green':
        out = '[green]' + text + f'[/green]'
    elif color == 'yellow':
        out = '[yellow]' + text + f'[/yellow]'
    else:
        raise ValueError("An unknown error has occurred.")
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
