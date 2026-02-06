from Options import Toggle, Range, Choice
from dataclasses import dataclass

BOARD_KEY = "aptestboard"
class aptestenabledOption(Toggle):
    """Enable or disable the AP Test Board in Mario Party 3."""
    display_name = "AP Test Board Enabled"
    default = True
    
class APteststarsOption(Range):
    """Set the number of stars required to win on the AP Test Board."""
    display_name = "AP Test Board Star Count"
    default = 10
    range_start = 6
    range_end = 20
@dataclass(init=False)
class OptionMixin:
    ap_test_board_enabled : aptestenabledOption
    ap_test_board_star_count : APteststarsOption