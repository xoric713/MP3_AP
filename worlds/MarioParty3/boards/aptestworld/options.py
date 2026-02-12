from Options import Toggle, Range, Choice
from dataclasses import dataclass

BOARD_KEY = "aptestboard"
class aptestenabledOption(Toggle):
    """Enable or disable the AP Test Board in Mario Party 3."""
    display_name = "AP Test Board Enabled"
    default = True
    
class APtestGameLength(Range):
    """Set the number of turns required to win on the AP Test Board."""
    display_name = "AP Test Board Game Length"
    default = 20
    range_start = 15
    range_end = 50
    
