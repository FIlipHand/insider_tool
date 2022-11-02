from colorama import Fore, Style


def get_colored_text(text: str, color: str) -> str:
    assert color == 'red' or color == 'green' or color == 'yellow'
    if color == 'red':
        out = Fore.RED + text + Style.RESET_ALL
    elif color == 'green':
        out = Fore.GREEN + text + Style.RESET_ALL
    elif color == 'yellow':
        out = Fore.YELLOW + text + Style.RESET_ALL
    else:
        raise ValueError("An unknown error has occurred.")
    return out
