import unittest
from contextlib import nullcontext as does_not_raise
from unittest.mock import patch, Mock

from game.exceptions import IncorrectFightResult, EnemyDown, GameOver
from game.game import Game
from game.scores import PlayerRecord
from settings import (
    MODE_NORMAL,
    MODE_HARD,
    DRAW,
    WIN,
    LOSE,
    PLAYER_HIT_POINTS,
    POINTS_FOR_FIGHT,
    POINTS_FOR_KILLING,
    PAPER,
    STONE,
    SCISSORS,
    HARD_MODE_MULTIPLIER
)


class TestGameInitAndInputMode(unittest.TestCase):

    def setUp(self):
        self.score_handler = Mock()

    @patch("builtins.input", side_effect=['Vlad', "1"])
    def test_game_init(self, mock_input):
        with does_not_raise():
            game = Game(self.score_handler)
        self.assertEqual(game.mode, MODE_NORMAL)

    @patch("builtins.input", side_effect=['Vlad', "2"])
    def test_game_init_hard(self, mock_input):
        with does_not_raise():
            game = Game(self.score_handler)
        self.assertEqual(game.mode, MODE_HARD)

    @patch("builtins.input", side_effect=['Vlad', "3", "1"])
    def test_game_init_incorrect_mode_int(self, mock_input):
        with does_not_raise():
            Game(self.score_handler)

    @patch("builtins.input", side_effect=['Vlad', "blabla", "1"])
    def test_game_init_incorrect_mode_str(self, mock_input):
        with does_not_raise():
            Game(self.score_handler)


class TestGameNewEnemy(unittest.TestCase):

    @patch("builtins.input", side_effect=['Vlad', "1"])
    def test_game_init(self, mock_input):
        game = Game(score_handler=Mock())
        game.new_enemy()
        self.assertEqual(game.enemy.level, 1)
        game.new_enemy()
        self.assertEqual(game.enemy.level, 2)


class TestHandleFightResult(unittest.TestCase):

    @patch("builtins.input", side_effect=['Vlad', "1"])
    def setUp(self, mock_input):
        self.game = Game(score_handler=Mock())
        self.game.new_enemy()

    def test_incorrect_fight_result(self):
        with self.assertRaises(IncorrectFightResult):
            self.game._handle_fight_result(5)

    def test_draw(self):
        self.game._handle_fight_result(DRAW)

    def test_lose(self):
        self.game._handle_fight_result(LOSE)
        self.assertEqual(self.game.player.lives, PLAYER_HIT_POINTS - 1)

    def test_lose_game_over(self):
        with self.assertRaises(GameOver):
            for i in range(PLAYER_HIT_POINTS):
                self.game._handle_fight_result(LOSE)
        self.assertEqual(self.game.player.lives, 0)

    def test_win(self):
        self.game.new_enemy()
        self.assertEqual(self.game.enemy.level, 2)
        self.assertEqual(self.game.enemy.lives, 2)
        self.game._handle_fight_result(WIN)
        self.assertEqual(self.game.enemy.lives, 1)
        self.assertEqual(self.game.player.score, POINTS_FOR_FIGHT)

    def test_win_enemy_down(self):
        with self.assertRaises(EnemyDown):
            self.game._handle_fight_result(WIN)
        self.assertEqual(self.game.enemy.lives, 0)
        self.assertEqual(self.game.player.score, POINTS_FOR_FIGHT + POINTS_FOR_KILLING)


class TestFight(unittest.TestCase):

    @patch("builtins.input", side_effect=['Vlad', "1"])
    def setUp(self, mock_input):
        self.game = Game(score_handler=Mock())
        self.game.new_enemy()

    @patch("game.game.Game._handle_fight_result")
    @patch("game.models.Player.attack")
    @patch("game.models.Enemy.attack")
    def test_fight_paper_paper(self, mock_enemy_attack, mock_player_attack, mock_fight_result):
        mock_player_attack.return_value = PAPER
        mock_enemy_attack.return_value = PAPER
        self.game._fight()
        mock_fight_result.assert_called_once_with(DRAW)

    @patch("game.game.Game._handle_fight_result")
    @patch("game.models.Player.attack")
    @patch("game.models.Enemy.attack")
    def test_fight_paper_scissors(self, mock_enemy_attack, mock_player_attack, mock_fight_result):
        mock_player_attack.return_value = PAPER
        mock_enemy_attack.return_value = SCISSORS
        self.game._fight()
        mock_fight_result.assert_called_once_with(LOSE)

    @patch("game.game.Game._handle_fight_result")
    @patch("game.models.Player.attack")
    @patch("game.models.Enemy.attack")
    def test_fight_paper_stone(self, mock_enemy_attack, mock_player_attack, mock_fight_result):
        mock_player_attack.return_value = PAPER
        mock_enemy_attack.return_value = STONE
        self.game._fight()
        mock_fight_result.assert_called_once_with(WIN)

    @patch("game.game.Game._handle_fight_result")
    @patch("game.models.Player.attack")
    @patch("game.models.Enemy.attack")
    def test_fight_scissors_paper(self, mock_enemy_attack, mock_player_attack, mock_fight_result):
        mock_player_attack.return_value = SCISSORS
        mock_enemy_attack.return_value = PAPER
        self.game._fight()
        mock_fight_result.assert_called_once_with(WIN)

    @patch("game.game.Game._handle_fight_result")
    @patch("game.models.Player.attack")
    @patch("game.models.Enemy.attack")
    def test_fight_scissors_stone(self, mock_enemy_attack, mock_player_attack, mock_fight_result):
        mock_player_attack.return_value = SCISSORS
        mock_enemy_attack.return_value = STONE
        self.game._fight()
        mock_fight_result.assert_called_once_with(LOSE)

    @patch("game.game.Game._handle_fight_result")
    @patch("game.models.Player.attack")
    @patch("game.models.Enemy.attack")
    def test_fight_scissors_scissors(self, mock_enemy_attack, mock_player_attack, mock_fight_result):
        mock_player_attack.return_value = SCISSORS
        mock_enemy_attack.return_value = SCISSORS
        self.game._fight()
        mock_fight_result.assert_called_once_with(DRAW)

    @patch("game.game.Game._handle_fight_result")
    @patch("game.models.Player.attack")
    @patch("game.models.Enemy.attack")
    def test_fight_stone_paper(self, mock_enemy_attack, mock_player_attack, mock_fight_result):
        mock_player_attack.return_value = STONE
        mock_enemy_attack.return_value = PAPER
        self.game._fight()
        mock_fight_result.assert_called_once_with(LOSE)

    @patch("game.game.Game._handle_fight_result")
    @patch("game.models.Player.attack")
    @patch("game.models.Enemy.attack")
    def test_fight_stone_scissors(self, mock_enemy_attack, mock_player_attack, mock_fight_result):
        mock_player_attack.return_value = STONE
        mock_enemy_attack.return_value = SCISSORS
        self.game._fight()
        mock_fight_result.assert_called_once_with(WIN)

    @patch("game.game.Game._handle_fight_result")
    @patch("game.models.Player.attack")
    @patch("game.models.Enemy.attack")
    def test_fight_stone_stone(self, mock_enemy_attack, mock_player_attack, mock_fight_result):
        mock_player_attack.return_value = STONE
        mock_enemy_attack.return_value = STONE
        self.game._fight()
        mock_fight_result.assert_called_once_with(DRAW)


class TestStartGame(unittest.TestCase):

    @patch("builtins.input", side_effect=['Vlad', "1"])
    def setUp(self, mock_input):
        self.game = Game(score_handler=Mock())

    @patch("game.models.Enemy.attack", side_effect=[STONE, STONE])
    @patch("game.models.Player.attack", side_effect=[SCISSORS, SCISSORS])
    def test_start_game_game_over_without_scores(self, mock_player_attack, mock_enemy_attack):
        self.game.start_game()
        self.assertEqual(self.game.player.lives, 0)
        self.assertEqual(self.game.enemy.lives, 1)
        self.assertEqual(self.game.player.score, 0)
        player_record = PlayerRecord("Vlad", MODE_NORMAL, 0)
        self.game.score_handler.game_record.add_record.assert_called_once_with(player_record)
        self.game.score_handler.write.assert_called_once()

    @patch("game.models.Enemy.attack", side_effect=[STONE, STONE, STONE])
    @patch("game.models.Player.attack", side_effect=[PAPER, SCISSORS, SCISSORS])
    def test_start_game_kill_1_enemy(self, mock_player_attack, mock_enemy_attack):
        self.game.start_game()
        self.assertEqual(self.game.player.lives, 0)
        self.assertEqual(self.game.enemy.lives, 2)
        scores = POINTS_FOR_FIGHT + POINTS_FOR_KILLING
        self.assertEqual(self.game.player.score, scores)
        player_record = PlayerRecord("Vlad", MODE_NORMAL, scores)
        self.game.score_handler.game_record.add_record.assert_called_once_with(player_record)
        self.game.score_handler.write.assert_called_once()

    @patch("game.models.Enemy.attack", side_effect=[STONE, STONE, STONE, STONE, STONE])
    @patch("game.models.Player.attack", side_effect=[PAPER, PAPER, PAPER, SCISSORS, SCISSORS])
    def test_start_game_kill_2_enemies(self, mock_player_attack, mock_enemy_attack):
        self.game.start_game()
        self.assertEqual(self.game.player.lives, 0)
        self.assertEqual(self.game.enemy.lives, 3)
        scores = POINTS_FOR_FIGHT * 3 + POINTS_FOR_KILLING * 2
        self.assertEqual(self.game.player.score, scores)
        player_record = PlayerRecord("Vlad", MODE_NORMAL, scores)
        self.game.score_handler.game_record.add_record.assert_called_once_with(player_record)
        self.game.score_handler.write.assert_called_once()


class TestStartGameHardMode(unittest.TestCase):

    @patch("builtins.input", side_effect=['Vlad', "2"])
    def setUp(self, mock_input):
        self.game = Game(score_handler=Mock())

    @patch("game.models.Enemy.attack", side_effect=[STONE, STONE])
    @patch("game.models.Player.attack", side_effect=[SCISSORS, SCISSORS])
    def test_start_game_game_over_without_scores(self, mock_player_attack, mock_enemy_attack):
        self.game.start_game()
        self.assertEqual(self.game.player.lives, 0)
        self.assertEqual(self.game.enemy.lives, 1 * HARD_MODE_MULTIPLIER)
        self.assertEqual(self.game.player.score, 0)
        player_record = PlayerRecord("Vlad", MODE_HARD, 0)
        self.game.score_handler.game_record.add_record.assert_called_once_with(player_record)
        self.game.score_handler.write.assert_called_once()

    @patch("game.models.Enemy.attack", side_effect=[STONE, STONE, STONE, STONE])
    @patch("game.models.Player.attack", side_effect=[PAPER, PAPER, SCISSORS, SCISSORS])
    def test_start_game_kill_1_enemy(self, mock_player_attack, mock_enemy_attack):
        self.game.start_game()
        self.assertEqual(self.game.player.lives, 0)
        self.assertEqual(self.game.enemy.lives, 2 * HARD_MODE_MULTIPLIER)
        scores = (POINTS_FOR_FIGHT * 2 + POINTS_FOR_KILLING) * HARD_MODE_MULTIPLIER
        self.assertEqual(self.game.player.score, scores)
        player_record = PlayerRecord("Vlad", MODE_HARD, scores)
        self.game.score_handler.game_record.add_record.assert_called_once_with(player_record)
        self.game.score_handler.write.assert_called_once()

    @patch("game.models.Enemy.attack", side_effect=[STONE, STONE, STONE, STONE, STONE, STONE, STONE, STONE])
    @patch("game.models.Player.attack", side_effect=[PAPER, PAPER, PAPER, PAPER, PAPER, PAPER, SCISSORS, SCISSORS])
    def test_start_game_kill_2_enemies(self, mock_player_attack, mock_enemy_attack):
        self.game.start_game()
        self.assertEqual(self.game.player.lives, 0)
        self.assertEqual(self.game.enemy.lives, 3 * HARD_MODE_MULTIPLIER)
        scores = (POINTS_FOR_FIGHT * 6 + POINTS_FOR_KILLING * 2) * HARD_MODE_MULTIPLIER
        self.assertEqual(self.game.player.score, scores)
        player_record = PlayerRecord("Vlad", MODE_HARD, scores)
        self.game.score_handler.game_record.add_record.assert_called_once_with(player_record)
        self.game.score_handler.write.assert_called_once()
