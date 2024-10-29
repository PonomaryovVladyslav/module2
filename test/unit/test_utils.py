from unittest import TestCase

from game.exceptions import IncorrectMenuOptionError
from game.utils import generate_input_help, generate_menu, generate_scores_title_row


class TestGenerateInputHelp(TestCase):

    def test_generate_input_help_main_menu(self):
        help_text = generate_input_help("main_menu")
        self.assertEqual(help_text, "----Main Menu----\nPlease select an option from the list:\n\n1: Play\n2: Score\n3: Exit\n")

    def test_generate_input_help_attacks(self):
        help_text = generate_input_help("attacks")
        self.assertEqual(help_text, "----Attack----\nPlease select an option from the list:\n\n1: Paper\n2: Stone\n3: Scissors\n0: Exit Game\n")

    def test_generate_input_help_mode(self):
        help_text = generate_input_help("mode")
        self.assertEqual(help_text, "----Mode----\nPlease select an option from the list:\n\n1: Normal\n2: Hard\n")

    def test_generate_input_help_incorrect(self):
        with self.assertRaises(IncorrectMenuOptionError):
            generate_input_help("some incorrect value")


class TestGenerateMenu(TestCase):

    def test_generate_menu_some_values(self):
        dict_to_test = {"1": "2", "3": 4}
        key = "some_key"
        help_text = generate_menu(dict_to_test, key)
        self.assertEqual(help_text, "None\nPlease select an option from the list:\n\n1: 2\n3: 4\n")


class TestGenerateScoresTitleRow(TestCase):

    def test_generate_scores_title_row_empty(self):
        self.assertEqual(generate_scores_title_row(), "NAME MODE      SCORE\n")

    def test_generate_scores_title_row_less_than_4(self):
        self.assertEqual(generate_scores_title_row(2), "NAME MODE      SCORE\n")

    def test_generate_scores_title_row_equal_4(self):
        self.assertEqual(generate_scores_title_row(4), "NAME MODE      SCORE\n")

    def test_generate_scores_title_row_big_than_4(self):
        self.assertEqual(generate_scores_title_row(10), "NAME      MODE      SCORE\n")