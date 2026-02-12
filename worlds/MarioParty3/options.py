from Options import PerGameCommonOptions
from dataclasses import dataclass
from .boards.Options import PlayerCharOption, COM1CharOption, COM2CharOption, COM3CharOption, ProgTurnsOption
from .boards.aptestworld.Options import aptestenabledOption, APtestGameLength


@dataclass
class MP3Options(PerGameCommonOptions):
    PlayerChar: PlayerCharOption
    COM1Char: COM1CharOption
    COM2Char: COM2CharOption
    COM3Char: COM3CharOption
    progturns: ProgTurnsOption
    ap_test_board_enabled : aptestenabledOption
    ap_test_board_turn_count : APtestGameLength