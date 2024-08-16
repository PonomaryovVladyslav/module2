"""
Module for reading and writing scores.
"""

from game.models import Player
from game.utils import generate_scores_title_row
from game.validations import validate_mode
from settings import MAX_RECORDS_NUMBER


class PlayerRecord:
    """
    Class, which contains one record
    """
    name: str
    mode: str
    score: int

    def __init__(self, name: str, mode: str, score: int) -> None:
        """
        Init
        :param name: player's name
        :param mode: mode of game
        :param score: player's score
        """
        validate_mode(mode)
        self.name = name
        self.mode = mode
        self.score = score

    @classmethod
    def from_player(cls, player: Player, mode: str) -> "PlayerRecord":
        """
        method to create record directly from player
        :param player: Player object
        :param mode: mode of game
        :return: Record object
        """
        validate_mode(mode)
        return PlayerRecord(name=player.name, mode=mode, score=player.score)

    def __eq__(self, other):
        """Method to compare two records only by name and mode"""
        return self.name == other.name and self.mode == other.mode

    def __gt__(self, other):
        """Method to find, which object contains bigger score"""
        return self.score > other.score

    def as_file_row(self, biggest_name_size: int) -> str:
        """
        Method to generate a row prepared to file
        :param biggest_name_size: biggest name into the list. To make table prettier
        :return: string, which is ready to write to file
        """
        name_column_size = 5 if biggest_name_size <= 4 else biggest_name_size
        return f'{self.name.ljust(name_column_size)}{self.mode.ljust(10)}{str(self.score).ljust(5)}\n'


class GameRecord:
    """
    Class, which contains all list of records
    """
    records: list[PlayerRecord]

    def __init__(self) -> None:
        """Init"""
        self.records = []

    def add_record(self, record: PlayerRecord) -> None:
        """
        Method to add a record to the records
        :param record: Record object

        If record not in the records list, it will be added.
        If record in, we have to check is current record bigger than existing.
        And keep record which is bigger
        """
        if record not in self.records:
            self.records.append(record)
            self._prepare_records_to_save()
        else:
            old_record = self.records[self.records.index(record)]
            if old_record < record:
                self.records.remove(old_record)
                self.records.append(record)
                self._prepare_records_to_save()
                print("Your record updated!")
            else:
                print("Your had better result!")

    def records_from_lines(self, lines: list[str]) -> None:
        """
        Read and store records from lines
        :param lines: line format is {Name mode score} which splitted by any amount of spaces
        """
        for line in lines:
            name, mode, score = line.strip().split()
            player_record = PlayerRecord(name, mode, int(score))
            self.records.append(player_record)

    def _prepare_records_to_save(self) -> None:
        """
        Prepare the records to save
        Sort by scores and remove records if amount bigger than max amount
        """
        records_to_save = sorted(self.records, reverse=True)
        self.records = records_to_save[:MAX_RECORDS_NUMBER]

    @property
    def biggest_name_size(self) -> int:
        """
        Max length of names +1
        Just to keep file pretty
        """
        return max([len(pr.name) for pr in self.records]) + 1 if self.records else 0


class ScoreHandler:
    """
    Class to handle scores (read/write/print)
    """
    game_record: GameRecord
    file_name: str

    def __init__(self, file_name: str) -> None:
        """Init"""
        self.game_record = GameRecord()
        self.file_name = file_name

    def read(self) -> None:
        """
        Try to read. If file exists read records. If not create new one only with headers
        """
        try:
            with open(self.file_name, "r") as f:
                lines = f.readlines()
                self.game_record.records_from_lines(lines[1:])
        except FileNotFoundError:
            with open(self.file_name, 'w') as file:
                file.write(generate_scores_title_row())

    def write(self) -> None:
        """Write to file headed and all records"""
        with open(self.file_name, 'w') as file:
            file.write(generate_scores_title_row(biggest_name_size=self.game_record.biggest_name_size))
            for record in self.game_record.records:
                file.write(record.as_file_row(biggest_name_size=self.game_record.biggest_name_size))

    def pretty_print(self) -> None:
        """To print stats pretty"""
        print(generate_scores_title_row())
        for record in self.game_record.records:
            print(record.as_file_row(biggest_name_size=self.game_record.biggest_name_size))
