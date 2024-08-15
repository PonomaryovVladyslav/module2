""" User defined Exceptions """


class GameOver(Exception):
    """Raised if player lost all lives"""


class EnemyDown(Exception):
    """Raised if enemy lost all lives"""


class QuitApp(Exception):
    """Raised if user send command to exit the unfinished game"""


class WhiteSpaceInputError(Exception):
    """Raised if user input contains white spaces"""


class EmptyInputError(Exception):
    """Raised if user input is an empty string"""


class IncorrectMenuOptionError(Exception):
    """Raised if menu option is incorrect """


class IncorrectAttackOptionError(Exception):
    """Raised if attack option is incorrect """


class IncorrectModeError(Exception):
    """Raised if mode is incorrect """


class IncorrectLevelError(Exception):
    """Raised if level is incorrect """


class IncorrectFightResult(Exception):
    """Raised if result of battle is incorrect """
