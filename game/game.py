""" This file is the entry file. Run it to start."""
from game.exceptions import (
    GameOver,
    EnemyDown,
    QuitApp,
    IncorrectMenuOptionError,
    IncorrectModeError
)
from game.models import Player, Enemy
from game.scores import ScoreHandler, PlayerRecord
from game.utils import generate_input_help
from game.validations import validate_fight_result, validate_input_menu, validate_input_mode
from settings import MODES, ATTACK_PAIRS_OUTCOME, PLAY, SCORE, EXIT, WIN, LOSE, DRAW, MAIN_MENU_OPTIONS, SCORE_FILENAME

__version__ = '1'


#

class Game:
    """
    The game class to start game
    """
    mode: str
    player: Player
    enemy: Enemy
    score_handler: ScoreHandler

    # TODO: Add score handler

    def __init__(self, score_handler: ScoreHandler):
        """
        Initialize the game
        """
        self.player = Player()
        self.input_mode()
        self.score_handler = score_handler
        self.score_handler.read()

    def input_mode(self) -> None:
        """
        Input and return game mode
        """
        while True:
            mode_input = input(generate_input_help("mode"))
            try:
                validate_input_mode(mode_input)
            except IncorrectModeError:
                print('Incorrect input.')
            else:
                self.mode = MODES[mode_input]
                break

    def new_enemy(self) -> None:
        """
        Create new enemy with new level
        """
        if hasattr(self, 'enemy'):
            level = self.enemy.level + 1
        else:
            level = 1
        self.enemy = Enemy(mode=self.mode, level=level)

    def print_status(self) -> None:
        """
        Prints the current game status to console
        """
        print(f"\nPlayer: {self.player.name}."
              f"\tMode: {self.mode}."
              f"\tPlayer Lives: {self.player.lives}."
              f"\tScore: {self.player.score}."
              f"\tLevel: {self.enemy.level}"
              f"\tEnemy's lives: {self.enemy.lives}")

    def _fight(self) -> None:
        """
        Resolves player's attack vs enemy's attack
        """
        enemy_attack = self.enemy.attack()
        player_attack = self.player.attack()
        print(f"Your attack: {player_attack}.  Enemy's attack: {enemy_attack}")
        fight_result = ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)]
        self._handle_fight_result(fight_result)

    def _handle_fight_result(self, fight_result: int) -> None:
        """
        Handles results of the fight
        """
        validate_fight_result(fight_result)
        if fight_result == WIN:
            print('You attacked successfully!')
            self.player.on_win_fight(self.mode)
            try:
                self.enemy.on_lose_fight()
            except EnemyDown:
                self.player.on_enemy_down(self.mode)
                raise
        elif fight_result == LOSE:
            print("You missed!")
            self.player.on_lose_fight()
        elif fight_result == DRAW:
            print("It's a draw!")

    def start_game(self) -> None:
        """
        Start game method
        """
        self.new_enemy()
        try:
            while True:
                self.print_status()
                try:
                    self._fight()
                except EnemyDown:
                    self.new_enemy()
                    print("\nNew enemy comes.")
        except GameOver:
            print('You lose!')
            player_record = PlayerRecord(self.player.name, self.mode, self.player.score)
            self.score_handler.game_record.add_record(player_record)
            self.score_handler.write()
        finally:
            self.print_status()



def main_menu_input() -> str:
    """
    Menu user input
    """
    while True:
        menu_choice = input(generate_input_help("main_menu"))
        try:
            validate_input_menu(menu_choice)
        except IncorrectMenuOptionError:
            print('Incorrect input. Please try again.')
        else:
            return MAIN_MENU_OPTIONS[menu_choice]


def main_menu() -> None:
    """
    Displays the main menu of the game
    """
    menu_choice = main_menu_input()
    score_handler = ScoreHandler(SCORE_FILENAME)
    # TODO: ADD SCORE HANDLER
    if menu_choice == PLAY:
        game = Game(score_handler)
        game.start_game()
    elif menu_choice == SCORE:
        score_handler.read()
        score_handler.pretty_print()
        main_menu()
    elif menu_choice == EXIT:
        raise QuitApp


def main():
    """
    Main game loop
    """
    try:
        main_menu()
    except QuitApp:
        print('Good buy!')
    except KeyboardInterrupt:
        print('Good buy!')
