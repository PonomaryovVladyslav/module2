""" Constants and settings used in the project """

# Player settings
PLAYER_LIVES = 2

# Scores settings
POINTS_FOR_FIGHT = 1
POINTS_FOR_KILLING = 5
HARD_MODE_MULTIPLIER = 2

# Main menu options
PLAY = "Play"
SCORE = "Score"
EXIT = "Exit"
MAIN_MENU_OPTIONS = {
    "1": PLAY,
    "2": SCORE,
    "3": EXIT
}

# Modes settings
MODE_NORMAL = 'Normal'
MODE_HARD = 'Hard'
MODES = {
    '1': MODE_NORMAL,
    '2': MODE_HARD
}

# Allowed attacks settings
PAPER = 'Paper'
STONE = 'Stone'
SCISSORS = 'Scissors'
ALLOWED_ATTACKS = {
    '1': PAPER,
    '2': STONE,
    '3': SCISSORS,
    '0': 'Exit Game'
}

# Fight result constants
WIN = 1
DRAW = 0
LOSE = -1

ATTACK_PAIRS_OUTCOME = {
    (PAPER, PAPER): DRAW,
    (PAPER, STONE): WIN,
    (PAPER, SCISSORS): LOSE,
    (STONE, PAPER): LOSE,
    (STONE, STONE): DRAW,
    (STONE, SCISSORS): WIN,
    (SCISSORS, PAPER): WIN,
    (SCISSORS, STONE): LOSE,
    (SCISSORS, SCISSORS): DRAW
}

INPUT_BASIC_TEXT = 'Please select an option from the list:\n'

BASIC_OPTION_TEXTS = {
    'main_menu': '----Main Menu----',
    'attacks': '----Attack----',
    'mode': '----Mode----'
}


# Score IO settings

SCORE_FILENAME = 'scores.txt'
MAX_RECORDS_NUMBER = 5