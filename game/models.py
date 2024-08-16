""" Module contains Enemy Class and Player Class"""

from random import randint

from game.exceptions import (
    GameOver,
    EnemyDown,
    QuitApp,
    WhiteSpaceInputError,
    EmptyInputError,
    IncorrectAttackOptionError)
from game.utils import generate_input_help
from game.validations import validate_input_attack, validate_name, validate_mode, validate_level
from settings import (
    ALLOWED_ATTACKS,
    MODE_NORMAL,
    PLAYER_HIT_POINTS,
    POINTS_FOR_FIGHT,
    POINTS_FOR_KILLING,
    HARD_MODE_MULTIPLIER
)


class Enemy:
    """
    Class represents the enemy bot player
    """
    lives: int
    level: int

    def __init__(self, mode: str, level: int):
        """
        Initializes the enemy instance
        """
        validate_mode(mode)
        validate_level(level)
        self.level = level
        self.lives = self.level if mode == MODE_NORMAL else self.level * HARD_MODE_MULTIPLIER

    @staticmethod
    def attack() -> str:
        """
        Randomly returns one of possible enemy's attack
        """
        return ALLOWED_ATTACKS[str(randint(1, 3))]

    def on_lose_fight(self) -> None:
        """
        Decrease enemy's lives
        """
        self.lives -= 1
        if self.lives == 0:
            raise EnemyDown


class Player:
    """
    Class describes user's player
    """
    name: str
    score: int
    lives: int

    def __init__(self):
        """
        Initializes the player instance
        """
        self.score = 0
        self.input_name()
        self.lives = PLAYER_HIT_POINTS

    def input_name(self) -> None:
        """
        Input and return player name
        """
        while True:
            name = input("Enter your name: ")
            try:
                validate_name(name)
                self.name = name
                break
            except WhiteSpaceInputError:
                print("Whitespaces are not allowed in the name.")
            except EmptyInputError:
                print('Name cannot be empty.')

    @staticmethod
    def attack() -> str:
        """
        Asks for user attack input
        """
        while True:
            attack_input = input(generate_input_help("attacks"))
            try:
                validate_input_attack(attack_input)
                if attack_input == '0':
                    raise QuitApp
                return ALLOWED_ATTACKS[attack_input]
            except IncorrectAttackOptionError:
                print('Incorrect input.')

    def on_lose_fight(self) -> None:
        """
        Decreases player's lives
        """
        self.lives -= 1
        if self.lives == 0:
            raise GameOver

    def on_win_fight(self, mode) -> None:
        """
        Adds score if successful fight
        """
        validate_mode(mode)
        self.score += POINTS_FOR_FIGHT if mode == MODE_NORMAL else POINTS_FOR_FIGHT * HARD_MODE_MULTIPLIER

    def on_enemy_down(self, mode):
        """
        Adds score on enemy down
        """
        print("Congratulation! Enemy down.")
        validate_mode(mode)
        self.score += POINTS_FOR_KILLING if mode == MODE_NORMAL else POINTS_FOR_KILLING * HARD_MODE_MULTIPLIER
