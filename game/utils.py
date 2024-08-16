"""File with utils"""
from game.exceptions import IncorrectMenuOptionError
from settings import INPUT_BASIC_TEXT, MAIN_MENU_OPTIONS, ALLOWED_ATTACKS, BASIC_OPTION_TEXTS, MODES


def generate_input_help(key: str) -> str:
    """
    Print text for menus
    :param key: main_menu, attacks, mode
    :return: text to print for player
    """
    match key:
        case "main_menu":
            return generate_menu(MAIN_MENU_OPTIONS, key)
        case "attacks":
            return generate_menu(ALLOWED_ATTACKS, key)
        case "mode":
            return generate_menu(MODES, key)
        case _:
            print("Incorrect menu option")
            raise IncorrectMenuOptionError


def generate_menu(menu: dict[str, str], key: str) -> str:
    """

    :param menu: dict with current chosen menu
    :param key: main_menu, attacks, mode
    :return: text to print for player
    """
    options = ''.join([f"{option}: {description}\n" for option, description in menu.items()])
    result = f"{BASIC_OPTION_TEXTS.get(key)}\n{INPUT_BASIC_TEXT}\n{options}"
    return result


def generate_scores_title_row(biggest_name_size: int = 0):
    name_column_size = 5 if biggest_name_size <= 4 else biggest_name_size
    return f'{"NAME".ljust(name_column_size)}{"MODE".ljust(10)}SCORE\n'
