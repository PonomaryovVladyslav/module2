import os
import unittest
from unittest.mock import patch, call

from main import main


class TestIntegration(unittest.TestCase):

    @patch('game.models.randint')
    @patch('builtins.input')
    @patch('builtins.print')
    @patch('game.game.SCORE_FILENAME', 'test_file_name.txt')
    def test_game_0_scores(self, mock_print, mock_input, mock_randint):
        mock_randint.side_effect = [1, 1]
        mock_input.side_effect = ['1', 'Vlad', '1', '2', '2']
        main()
        calls = [call("\nPlayer: Vlad.\tMode: Normal.\tPlayer Lives: 0.\tScore: 0.\tLevel: 1\tEnemy's lives: 1"),
                 call('Good buy!')]
        mock_print.assert_has_calls(calls, any_order=True)


    @patch('game.models.randint')
    @patch('builtins.input')
    @patch('builtins.print')
    @patch('game.game.SCORE_FILENAME', 'test_file_name.txt')
    def test_game_not_0_scores(self, mock_print, mock_input, mock_randint):
        mock_randint.side_effect = [2, 1, 1]
        mock_input.side_effect = ['1', 'Vlad', '1', '1', '2', '2']
        main()
        calls = [call("\nPlayer: Vlad.\tMode: Normal.\tPlayer Lives: 0.\tScore: 6.\tLevel: 2\tEnemy's lives: 2"),
                 call('Good buy!')]
        mock_print.assert_has_calls(calls, any_order=True)


    def tearDown(self):
        os.remove('test_file_name.txt')
