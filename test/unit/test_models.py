import unittest
from contextlib import nullcontext as does_not_raise
from unittest.mock import patch

from game.exceptions import IncorrectLevelError, IncorrectModeError, EnemyDown, GameOver, QuitApp
from game.models import Enemy, Player
from settings import PLAYER_HIT_POINTS, ATTACK_PAIRS_OUTCOME, PAPER, STONE, SCISSORS, WIN, LOSE, DRAW, \
    POINTS_FOR_KILLING, \
    HARD_MODE_MULTIPLIER


class TestEnemyCreation(unittest.TestCase):
    def test_enemy_creation_incorrect_mode(self):
        with self.assertRaises(IncorrectModeError):
            Enemy(mode='wrong', level=1)

    def test_enemy_creation_incorrect_level_str(self):
        with self.assertRaises(IncorrectLevelError):
            Enemy(mode='Normal', level='wrong')

    def test_enemy_creation_incorrect_level_minus(self):
        with self.assertRaises(IncorrectLevelError):
            Enemy(mode='Normal', level=-4)

    def test_enemy_creation_incorrect_level_and_mode(self):
        with self.assertRaises(IncorrectModeError):
            Enemy(mode='wrong', level=-4)

    def test_enemy_creation_success(self):
        with does_not_raise():
            Enemy(mode='Normal', level=1)


class TestEnemyDecreaseLives(unittest.TestCase):

    def test_enemy_not_died(self):
        enemy = Enemy(mode='Normal', level=3)
        with does_not_raise():
            enemy.on_lose_fight()
        self.assertEqual(enemy.lives, 2)

    def test_enemy_died(self):
        enemy = Enemy(mode='Normal', level=3)
        with self.assertRaises(EnemyDown):
            enemy.on_lose_fight()
            enemy.on_lose_fight()
            enemy.on_lose_fight()
        self.assertEqual(enemy.lives, 0)


class TestPlayerCreation(unittest.TestCase):
    @patch('builtins.input')
    def test_player_creation(self, mock_input):
        mock_input.return_value = 'Vlad'
        with does_not_raise():
            player = Player()
        self.assertEqual(player.name, 'Vlad')

    @patch('builtins.input')
    def test_player_creation_empty_name(self, mock_input):
        mock_input.side_effect = ['', 'Vlad']
        with does_not_raise():
            player = Player()
        self.assertEqual(player.name, 'Vlad')
        self.assertEqual(mock_input.call_count, 2)

    @patch('builtins.input')
    def test_player_creation_space_in_name(self, mock_input):
        mock_input.side_effect = ['test test', 'Vlad']
        with does_not_raise():
            player = Player()
        self.assertEqual(player.name, 'Vlad')
        self.assertEqual(mock_input.call_count, 2)


class TestPlayerAttack(unittest.TestCase):
    @patch('game.utils.generate_input_help')
    @patch('builtins.input')
    def test_player_attack_quit(self, mock_input, mock_input_generator):
        mock_input.side_effect = ['Vlad', '0']
        mock_input_generator.text.return_value = "doesn't matter"
        with self.assertRaises(QuitApp):
            player = Player()
            player.attack()

    @patch('game.utils.generate_input_help')
    @patch('builtins.input')
    def test_player_attack_incorrect(self, mock_input, mock_input_generator):
        mock_input.side_effect = ['Vlad', 'wrong', '1']
        mock_input_generator.text.return_value = "doesn't matter"
        with does_not_raise():
            player = Player()
            player.attack()
        self.assertEqual(mock_input.call_count, 3)

    @patch('game.utils.generate_input_help')
    @patch('builtins.input')
    def test_player_attack_correct(self, mock_input, mock_input_generator):
        mock_input.side_effect = ['Vlad', '1']
        mock_input_generator.text.return_value = "doesn't matter"
        with does_not_raise():
            player = Player()
            player.attack()
        self.assertEqual(mock_input.call_count, 2)


class TestPlayerLoseLives(unittest.TestCase):
    @patch('builtins.input')
    def test_player_lose_lives(self, mock_input):
        mock_input.side_effect = ['Vlad']
        with does_not_raise():
            player = Player()
            player.on_lose_fight()
        self.assertEqual(player.lives, PLAYER_HIT_POINTS - 1)

    @patch('builtins.input')
    def test_player_lose_lives_and_die(self, mock_input):
        mock_input.side_effect = ['Vlad']
        with self.assertRaises(GameOver):
            player = Player()
            for _ in range(PLAYER_HIT_POINTS):
                player.on_lose_fight()
        self.assertEqual(player.lives, 0)


class TestPlayerOnWinFight(unittest.TestCase):
    @patch('builtins.input')
    def test_player_win_fight_incorrect_mode(self, mock_input):
        mock_input.side_effect = ['Vlad']
        with self.assertRaises(IncorrectModeError):
            player = Player()
            player.on_win_fight('wrong')

    @patch('builtins.input')
    def test_player_win_fight_normal_mode(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        player.on_win_fight('Normal')
        self.assertEqual(player.score, 1)

    @patch('builtins.input')
    def test_player_win_fight_hard_mode(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        player.on_win_fight('Hard')
        self.assertEqual(player.score, 2)

    @patch('builtins.input')
    def test_player_win_fight_normal_mode_twice(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        player.on_win_fight('Normal')
        player.on_win_fight('Normal')
        self.assertEqual(player.score, 2)

    @patch('builtins.input')
    def test_player_win_fight_hard_mode_twice(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        player.on_win_fight('Hard')
        player.on_win_fight('Hard')
        self.assertEqual(player.score, 4)


class TestPlayerOnEnemyDown(unittest.TestCase):
    @patch('builtins.input')
    def test_player_win_fight_incorrect_mode(self, mock_input):
        mock_input.side_effect = ['Vlad']
        with self.assertRaises(IncorrectModeError):
            player = Player()
            player.on_enemy_down('wrong')

    @patch('builtins.input')
    def test_player_win_fight_normal_mode(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        player.on_enemy_down('Normal')
        self.assertEqual(player.score, POINTS_FOR_KILLING)

    @patch('builtins.input')
    def test_player_win_fight_hard_mode(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        player.on_enemy_down('Hard')
        self.assertEqual(player.score, POINTS_FOR_KILLING * HARD_MODE_MULTIPLIER)

    @patch('builtins.input')
    def test_player_win_fight_normal_mode_twice(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        player.on_enemy_down('Normal')
        player.on_enemy_down('Normal')
        self.assertEqual(player.score, POINTS_FOR_KILLING * 2)

    @patch('builtins.input')
    def test_player_win_fight_hard_mode_twice(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        player.on_enemy_down('Hard')
        player.on_enemy_down('Hard')
        self.assertEqual(player.score, POINTS_FOR_KILLING * HARD_MODE_MULTIPLIER * 2)


class TestAttackPairs(unittest.TestCase):
    def test_paper_paper(self):
        player_attack = PAPER
        enemy_attack = PAPER
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)], DRAW)

    def test_paper_stone(self):
        player_attack = PAPER
        enemy_attack = STONE
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)], WIN)

    def test_paper_scissors(self):
        player_attack = PAPER
        enemy_attack = SCISSORS
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)], LOSE)

    def test_scissios_paper(self):
        player_attack = SCISSORS
        enemy_attack = PAPER
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)], WIN)

    def test_scissors_stone(self):
        player_attack = SCISSORS
        enemy_attack = STONE
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)], LOSE)

    def test_scissors_scissors(self):
        player_attack = SCISSORS
        enemy_attack = SCISSORS
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)], DRAW)

    def test_stone_paper(self):
        player_attack = STONE
        enemy_attack = PAPER
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)], LOSE)

    def test_stone_scissors(self):
        player_attack = STONE
        enemy_attack = SCISSORS
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)], WIN)

    def test_stone_stone(self):
        player_attack = STONE
        enemy_attack = STONE
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)], DRAW)
