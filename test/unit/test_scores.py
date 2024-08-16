from contextlib import nullcontext as does_not_raise
from unittest import TestCase
from unittest.mock import patch, mock_open, Mock, call

from game.exceptions import IncorrectModeError
from game.models import Player
from game.scores import PlayerRecord, GameRecord, ScoreHandler
from settings import MODE_NORMAL, MODE_HARD

DEFAULT_EXPECTED_RECORDS = [
    PlayerRecord("Vlad", MODE_NORMAL, 30),
    PlayerRecord("Vlad1", MODE_NORMAL, 25),
    PlayerRecord("Vlad2", MODE_NORMAL, 20),
    PlayerRecord("Vlad", MODE_HARD, 15),
    PlayerRecord("Vlad1", MODE_HARD, 10),
]


class TestPlayerRecordInit(TestCase):

    def test_init_success_normal(self):
        with does_not_raise():
            PlayerRecord("Vlad", MODE_NORMAL, 10)

    def test_init_success_hard(self):
        with does_not_raise():
            PlayerRecord("Vlad", MODE_HARD, 20)

    def test_init_failed(self):
        with self.assertRaises(IncorrectModeError):
            PlayerRecord("Vlad", "random value", 20)


class TestPlayerRecordInitFromPlayer(TestCase):

    @patch("builtins.input", side_effect=["Vlad"])
    def setUp(self, mock_input):
        self.player = Player()

    def test_init_success_normal(self):
        with does_not_raise():
            PlayerRecord.from_player(self.player, MODE_NORMAL)

    def test_init_success_hard(self):
        with does_not_raise():
            PlayerRecord.from_player(self.player, MODE_HARD)

    def test_init_failed(self):
        with self.assertRaises(IncorrectModeError):
            PlayerRecord.from_player(self.player, "some_random")


class TestPlayerRecordEq(TestCase):

    def test_equal(self):
        pr1 = PlayerRecord("Vlad", MODE_NORMAL, 10)
        pr2 = PlayerRecord("Vlad", MODE_NORMAL, 20)
        self.assertEqual(pr1, pr2)

    def test_not_equal_mode(self):
        pr1 = PlayerRecord("Vlad", MODE_NORMAL, 10)
        pr2 = PlayerRecord("Vlad", MODE_HARD, 20)
        self.assertNotEqual(pr1, pr2)

    def test_not_equal_name(self):
        pr1 = PlayerRecord("Vlad", MODE_NORMAL, 10)
        pr2 = PlayerRecord("Kate", MODE_NORMAL, 20)
        self.assertNotEqual(pr1, pr2)

    def test_not_equal_all(self):
        pr1 = PlayerRecord("Vlad", MODE_NORMAL, 10)
        pr2 = PlayerRecord("Kate", MODE_HARD, 20)
        self.assertNotEqual(pr1, pr2)


class TestPlayerRecordGt(TestCase):

    def test_equal(self):
        pr1 = PlayerRecord("Vlad", MODE_NORMAL, 10)
        pr2 = PlayerRecord("Kate", MODE_HARD, 10)
        self.assertFalse(pr1 > pr2)

    def test_first_bigger(self):
        pr1 = PlayerRecord("Vlad", MODE_NORMAL, 20)
        pr2 = PlayerRecord("Vlad", MODE_HARD, 10)
        self.assertTrue(pr1 > pr2)

    def test_second_bigger(self):
        pr1 = PlayerRecord("Vlad", MODE_NORMAL, 10)
        pr2 = PlayerRecord("Kate", MODE_NORMAL, 20)
        self.assertTrue(pr1 < pr2)


class TestPlayerRecordAsFileRow(TestCase):

    def setUp(self):
        self.pr = PlayerRecord("Vlad", MODE_NORMAL, 10)

    def test_as_file_row_value_2(self):
        self.assertEqual(self.pr.as_file_row(2), "Vlad Normal    10   \n")

    def test_as_file_row_value_4(self):
        self.assertEqual(self.pr.as_file_row(4), "Vlad Normal    10   \n")

    def test_as_file_row_value_6(self):
        self.assertEqual(self.pr.as_file_row(6), "Vlad  Normal    10   \n")


class TestGameRecordInit(TestCase):

    def test_init_success_normal(self):
        game_record = GameRecord()
        self.assertEqual(len(game_record.records), 0)


class TestGameRecordRecordsFromLines(TestCase):

    def test_from_lines(self):
        lines = [
            "Vlad     Normal     30",
            "Vlad1     Normal     25",
            "Vlad2     Normal     20",
            "Vlad     Hard     15",
            "Vlad1     Hard     10",
        ]
        game_record = GameRecord()
        game_record.records_from_lines(lines)
        for expected_record in DEFAULT_EXPECTED_RECORDS:
            self.assertIn(expected_record, game_record.records)


class TestGameRecordSortRecords(TestCase):

    def test_sort(self):
        lines = [
            "Vlad     Hard     15",
            "Vlad1     Hard     10",
            "Vlad     Normal     30",
            "Vlad2     Normal     20",
            "Vlad1     Normal     25",

        ]
        game_record = GameRecord()
        game_record.records_from_lines(lines)
        game_record._prepare_records_to_save()
        self.assertEqual(game_record.records, DEFAULT_EXPECTED_RECORDS)


class TestGameRecordCutAndSort(TestCase):

    def test_sort_and_cut(self):
        lines = [
            "Vlad     Hard     15",
            "Vlad1     Hard     10",
            "Vlad4     Normal     0",
            "Vlad     Normal     30",
            "Vlad2     Normal     20",
            "Vlad1     Normal     25",
            "Vlad3     Normal     4",
        ]
        game_record = GameRecord()
        game_record.records_from_lines(lines)
        game_record._prepare_records_to_save()
        self.assertEqual(game_record.records, DEFAULT_EXPECTED_RECORDS)


class TestGameRecordBiggestNameSize(TestCase):

    def test_biggest_name_size_property_4(self):
        lines = [
            "Vlad     Hard     15",
        ]
        game_record = GameRecord()
        game_record.records_from_lines(lines)
        self.assertEqual(game_record.biggest_name_size, 5)

    def test_biggest_name_size_property_10(self):
        lines = [
            "Vlad     Hard     15",
            "Vlad123456     Hard     15",
        ]
        game_record = GameRecord()
        game_record.records_from_lines(lines)
        self.assertEqual(game_record.biggest_name_size, 11)


class TestGameRecordAddRecord(TestCase):

    def setUp(self):
        lines = [
            "Vlad     Normal     30",
            "Vlad1     Normal     25",
            "Vlad2     Normal     20",
            "Vlad     Hard     15",
            "Vlad1     Hard     10",
        ]
        self.game_record = GameRecord()
        self.game_record.records_from_lines(lines)

    def test_add_another_record_bigger(self):
        player_record = PlayerRecord("Name", MODE_NORMAL, 50)
        self.game_record.add_record(player_record)

        expected_records = [
            PlayerRecord("Name", MODE_NORMAL, 50),
            PlayerRecord("Vlad", MODE_NORMAL, 30),
            PlayerRecord("Vlad1", MODE_NORMAL, 25),
            PlayerRecord("Vlad2", MODE_NORMAL, 20),
            PlayerRecord("Vlad", MODE_HARD, 15),
        ]
        self.assertEqual(self.game_record.records, expected_records)

    def test_add_another_record_middle(self):
        player_record = PlayerRecord("Name", MODE_NORMAL, 24)
        self.game_record.add_record(player_record)

        expected_records = [
            PlayerRecord("Vlad", MODE_NORMAL, 30),
            PlayerRecord("Vlad1", MODE_NORMAL, 25),
            PlayerRecord("Name", MODE_NORMAL, 24),
            PlayerRecord("Vlad2", MODE_NORMAL, 20),
            PlayerRecord("Vlad", MODE_HARD, 15),
        ]
        self.assertEqual(self.game_record.records, expected_records)

    def test_add_another_record_smaller(self):
        player_record = PlayerRecord("Name", MODE_NORMAL, 9)
        self.game_record.add_record(player_record)
        self.assertEqual(self.game_record.records, DEFAULT_EXPECTED_RECORDS)

    def test_add_record_to_override_smaller(self):
        player_record = PlayerRecord("Vlad", MODE_NORMAL, 20)
        self.game_record.add_record(player_record)
        self.assertEqual(self.game_record.records, DEFAULT_EXPECTED_RECORDS)

    def test_add_record_to_override_bigger(self):
        player_record = PlayerRecord("Vlad", MODE_NORMAL, 50)
        self.game_record.add_record(player_record)

        expected_records = [
            PlayerRecord("Vlad", MODE_NORMAL, 50),
            PlayerRecord("Vlad1", MODE_NORMAL, 25),
            PlayerRecord("Vlad2", MODE_NORMAL, 20),
            PlayerRecord("Vlad", MODE_HARD, 15),
            PlayerRecord("Vlad1", MODE_HARD, 10),
        ]
        self.assertEqual(self.game_record.records, expected_records)


class TestScoreHandlerInit(TestCase):

    def test_init(self):
        sh = ScoreHandler("some_file_name.txt")
        self.assertEqual(sh.file_name, "some_file_name.txt")


class TestScoreHandlerRead(TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="header\nline1\nline2\n")
    def test_read_existing_file(self, mock_open):
        mock_game_record = Mock()
        with patch('game.scores.GameRecord', return_value=mock_game_record):
            handler = ScoreHandler("test_file.txt")
            handler.read()

            mock_open.assert_called_once_with("test_file.txt", "r")
            mock_game_record.records_from_lines.assert_called_once_with(["line1\n", "line2\n"])

    @patch("builtins.open", new_callable=mock_open)
    def test_read_nonexistent_file(self, mock_o):
        mock_o.side_effect = [FileNotFoundError, mock_o()]
        mock_game_record = Mock()

        with patch('game.scores.GameRecord', return_value=mock_game_record):
            handler = ScoreHandler("test_file.txt")
            handler.read()
            calls = [call('test_file.txt', 'r'), call('test_file.txt', 'w'), call().write('NAME MODE      SCORE\n')]
            mock_o.assert_has_calls(calls, any_order=True)
            mock_game_record.records_from_lines.assert_not_called()


class TestScoreHandlerWrite(TestCase):

    def setUp(self):
        self.score_handler = ScoreHandler("test_file.txt")

    @patch("builtins.open", new_callable=mock_open)
    def test_write_0_rows(self, mock_o):
        self.score_handler.write()
        calls = [call().write('NAME MODE      SCORE\n')]
        mock_o.assert_has_calls(calls, any_order=True)
        self.assertEqual(mock_o.call_count, 1)

    @patch("builtins.open", new_callable=mock_open)
    def test_write_2_rows(self, mock_o):
        lines = [
            "Vlad     Normal     30",
            "Vlad1     Normal     25",
        ]
        self.score_handler.game_record.records_from_lines(lines)
        self.score_handler.write()
        calls = [
            call().write('NAME  MODE      SCORE\n'),
            call().write('Vlad  Normal    30   \n'),
            call().write('Vlad1 Normal    25   \n'),
        ]
        mock_o.assert_has_calls(calls, any_order=True)


class TestScoreHandlerPrettyPrint(TestCase):

    @patch("builtins.print")
    def test_pretty_print(self, mock_print):
        score_handler = ScoreHandler("test_file.txt")
        lines = [
            "Vlad     Normal     30",
            "Vlad1     Normal     25",
        ]
        score_handler.game_record.records_from_lines(lines)
        score_handler.pretty_print()
        calls = [
            call('NAME MODE      SCORE\n'),
            call('Vlad  Normal    30   \n'),
            call('Vlad1 Normal    25   \n'),
        ]
        mock_print.assert_has_calls(calls, any_order=True)
