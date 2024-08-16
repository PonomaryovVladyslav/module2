from game.models import Player
from game.utils import generate_scores_title_row
from game.validations import validate_mode
from settings import MAX_RECORDS_NUMBER


class PlayerRecord:
    name: str
    mode: str
    score: int

    def __init__(self, name: str, mode: str, score: int):
        validate_mode(mode)
        self.name = name
        self.mode = mode
        self.score = score

    @classmethod
    def from_player(cls, player: Player, mode: str) -> "PlayerRecord":
        validate_mode(mode)
        return PlayerRecord(name=player.name, mode=mode, score=player.score)

    def __eq__(self, other):
        return self.name == other.name and self.mode == other.mode

    def __gt__(self, other):
        return self.score > other.score

    def as_file_row(self, biggest_name_size: int) -> str:
        name_column_size = 5 if biggest_name_size <= 4 else biggest_name_size
        return f'{self.name.ljust(name_column_size)}{self.mode.ljust(10)}{str(self.score).ljust(5)}\n'


class GameRecord:
    records: list[PlayerRecord]

    def __init__(self):
        self.records = []

    def add_record(self, record: PlayerRecord):
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

    def records_from_lines(self, lines: list[str]):
        for line in lines:
            name, mode, score = line.strip().split()
            player_record = PlayerRecord(name, mode, int(score))
            self.records.append(player_record)

    def _prepare_records_to_save(self):
        """
        Prepare the records to save
        """
        records_to_save = sorted(self.records, reverse=True)
        self.records = records_to_save[:MAX_RECORDS_NUMBER]

    @property
    def biggest_name_size(self):
        return max([len(pr.name) for pr in self.records]) + 1 if self.records else 0


class ScoreHandler:
    game_record: GameRecord
    file_name: str

    def __init__(self, file_name: str):
        self.game_record = GameRecord()
        self.file_name = file_name

    def read(self):
        try:
            with open(self.file_name, "r") as f:
                lines = f.readlines()
                self.game_record.records_from_lines(lines[1:])
        except FileNotFoundError:
            with open(self.file_name, 'w') as file:
                file.write(generate_scores_title_row())

    def write(self):
        with open(self.file_name, 'w') as file:
            file.write(generate_scores_title_row(biggest_name_size=self.game_record.biggest_name_size))
            for record in self.game_record.records:
                file.write(record.as_file_row(biggest_name_size=self.game_record.biggest_name_size))

    def pretty_print(self):
        print(generate_scores_title_row())
        for record in self.game_record.records:
            print(record.as_file_row(biggest_name_size=self.game_record.biggest_name_size))
