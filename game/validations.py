from game.exceptions import WhiteSpaceInputError, EmptyInputError, IncorrectModeError, IncorrectLevelError, \
    IncorrectFightResult, IncorrectMenuOptionError, IncorrectAttackOptionError
from settings import MODES, ALLOWED_ATTACKS, ATTACK_PAIRS_OUTCOME, MAIN_MENU_OPTIONS


def validate_name(name: str) -> None:
    """
    Validates user input name
    :param name: - name to validate
    """
    if ' ' in name:
        raise WhiteSpaceInputError
    elif not name:
        raise EmptyInputError


def validate_mode(mode: str) -> None:
    """
    Validate mode
    :param mode: - mode to validate
    """
    if mode not in MODES.values():
        raise IncorrectModeError


def validate_level(level: int) -> None:
    """
    Validate mode
    :param level: - level to validate
    """
    try:
        if not isinstance(level, int) or level <= 0:
            raise IncorrectLevelError
    except ValueError:
        raise IncorrectLevelError


def validate_fight_result(result: int) -> None:
    """
    Validate result of battle
    :param result: should be one of [1, 0, -1]
    """
    if result not in set(ATTACK_PAIRS_OUTCOME.values()):
        raise IncorrectFightResult


def validate_input_mode(mode_input: str) -> None:
    """
    Validate mode input
    :param mode_input: - mode of the game
    :return: True if mode in allowed modes, False otherwise
    """
    if mode_input not in MODES:
        raise IncorrectModeError


def validate_input_menu(menu_input: str) -> None:
    """
    Validate menu user input
    :param menu_input: - menu user input
    :return: True if menu in allowed modes, False otherwise
    """
    if menu_input not in MAIN_MENU_OPTIONS:
        raise IncorrectMenuOptionError


def validate_input_attack(attack_input: str) -> None:
    """
    Validate attack input
    :param attack_input: - attack user input
    :return: True if attack_input in allowed attacks, False otherwise
    """
    if attack_input not in ALLOWED_ATTACKS:
        raise IncorrectAttackOptionError
