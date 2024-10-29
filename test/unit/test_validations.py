import unittest
from contextlib import nullcontext as does_not_raise

from game.exceptions import (
    WhiteSpaceInputError,
    EmptyInputError,
    IncorrectModeError,
    IncorrectLevelError,
    IncorrectFightResult, IncorrectMenuOptionError, IncorrectAttackOptionError
)
from game.validations import (
    validate_mode,
    validate_name,
    validate_fight_result,
    validate_level,
    validate_input_menu,
    validate_input_mode,
    validate_input_attack
)
from settings import MODE_NORMAL, MODE_HARD


class TestValidateName(unittest.TestCase):
    def test_validate_name_valid(self):
        with does_not_raise():
            validate_name('name')

    def test_validate_name_invalid_empty(self):
        with self.assertRaises(EmptyInputError):
            validate_name('')

    def test_validate_name_invalid_space(self):
        with self.assertRaises(WhiteSpaceInputError):
            validate_name('bla bla')


class TestValidateMode(unittest.TestCase):
    def test_validate_mode_valid_normal(self):
        with does_not_raise():
            validate_mode(MODE_NORMAL)

    def test_validate_mode_valid_hard(self):
        with does_not_raise():
            validate_mode(MODE_HARD)

    def test_validate_mode_invalid(self):
        with self.assertRaises(IncorrectModeError):
            validate_mode('wrong')


class TestValidateLevel(unittest.TestCase):
    def test_validate_level_valid(self):
        with does_not_raise():
            validate_level(4)

    def test_validate_level_invalid_negative(self):
        with self.assertRaises(IncorrectLevelError):
            validate_level(-5)

    def test_validate_level_invalid_str(self):
        with self.assertRaises(IncorrectLevelError):
            validate_level('text')

    def test_validate_level_invalid_num(self):
        with self.assertRaises(IncorrectLevelError):
            validate_level('4')


class TestValidateFightResult(unittest.TestCase):
    def test_validate_incorrect_string(self):
        with self.assertRaises(IncorrectFightResult):
            validate_fight_result("aaa")

    def test_validate_incorrect(self):
        with self.assertRaises(IncorrectFightResult):
            validate_fight_result(2)

    def test_validate_1(self):
        with does_not_raise():
            validate_fight_result(1)

    def test_validate_0(self):
        with does_not_raise():
            validate_fight_result(0)

    def test_validate_negative_1(self):
        with does_not_raise():
            validate_fight_result(-1)


class TestValidateInputMode(unittest.TestCase):

    def test_invalid(self):
        with self.assertRaises(IncorrectModeError):
            validate_input_mode('5')

    def test_valid_1(self):
        with does_not_raise():
            validate_input_mode('1')

    def test_valid_2(self):
        with does_not_raise():
            validate_input_mode('2')


class TestIsValidInputMenu(unittest.TestCase):

    def test_invalid(self):
        with self.assertRaises(IncorrectMenuOptionError):
            validate_input_menu('5')

    def test_valid_1(self):
        with does_not_raise():
            validate_input_menu('1')

    def test_valid_2(self):
        with does_not_raise():
            validate_input_menu('2')

    def test_valid_3(self):
        with does_not_raise():
            validate_input_menu('3')

class TestIsValidInputAttack(unittest.TestCase):

    def test_invalid(self):
        with self.assertRaises(IncorrectAttackOptionError):
            validate_input_attack('5')

    def test_valid_1(self):
        with does_not_raise():
            validate_input_attack('1')

    def test_valid_2(self):
        with does_not_raise():
            validate_input_attack('2')

    def test_valid_3(self):
        with does_not_raise():
            validate_input_attack('3')

    def test_valid_0(self):
        with does_not_raise():
            validate_input_attack('0')
