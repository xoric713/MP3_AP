from Options import PerGameCommonOptions
from .boards.registry import iter_board_option_mixins
from dataclasses import dataclass

_mixins = list(iter_board_option_mixins())

Boardmixin = type("MP3Options", tuple(_mixins), {})

@dataclass
class MP3Options(PerGameCommonOptions, Boardmixin):
    pass