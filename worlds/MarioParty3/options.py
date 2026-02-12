from Options import PerGameCommonOptions
from .boards.registry import iter_board_option_mixins
from dataclasses import dataclass

_mixins = list(iter_board_option_mixins())

Boardmixin = type("MP3Options", tuple(_mixins), {})

@dataclass
class MP3Options(PerGameCommonOptions):
    PlayerChar: PlayerCharOption
    COM1Char: COM1CharOption
    COM2Char: COM2CharOption
    COM3Char: COM3CharOption
    progturns: ProgTurnsOption
    ap_test_board_enabled : aptestenabledOption
    ap_test_board_turn_count : APtestGameLength