from Options import Toggle, Range, Choice

BOARD_KEY = "Global"
class PlayerCharOption(Choice):
    """Choose which character to play as.
    Always_choose is the same as vanilla behavior
    Random_Per_Game chooses a random character per game
    Random_Always chooses a random character every time it can change characters."""
    display_name = "Player Character"
    option_Always_choose = 0
    option_Mario = 1
    option_Luigi = 2
    option_Peach = 3
    option_Yoshi = 4
    option_Wario = 5
    option_DonkeyKong = 6
    option_Waluigi = 7
    option_Daisy = 8
    option_Random_Per_Game = 9
    option_Random_Always = 10
    default = 0
class COM1CharOption(Choice):
    """Choose which character COM1 plays as.
    Always_choose is the same as vanilla behavior
    Random_Per_Game chooses a random character per game
    Random_Always chooses a random character every time it can change characters."""
    display_name = "COM1 Character"
    option_Always_choose = 0
    option_Mario = 1
    option_Luigi = 2
    option_Peach = 3
    option_Yoshi = 4
    option_Wario = 5
    option_DonkeyKong = 6
    option_Waluigi = 7
    option_Daisy = 8
    option_Random_Per_Game = 9
    option_Random_Always = 10
    default = 0
class COM2CharOption(Choice):
    """Choose which character COM2 plays as.
    Always_choose is the same as vanilla behavior
    Random_Per_Game chooses a random character per game
    Random_Always chooses a random character every time it can change characters."""
    display_name = "COM2 Character"
    option_Always_choose = 0
    option_Mario = 1
    option_Luigi = 2
    option_Peach = 3
    option_Yoshi = 4
    option_Wario = 5
    option_DonkeyKong = 6
    option_Waluigi = 7
    option_Daisy = 8
    option_Random_Per_Game = 9
    option_Random_Always = 10
    default = 0
class COM3CharOption(Choice):
    """Choose which character COM3 plays as.
    Always_choose is the same as vanilla behavior
    Random_Per_Game chooses a random character per game
    Random_Always chooses a random character every time it can change characters."""
    display_name = "COM3 Character"
    option_Always_choose = 0
    option_Mario = 1
    option_Luigi = 2
    option_Peach = 3
    option_Yoshi = 4
    option_Wario = 5
    option_DonkeyKong = 6
    option_Waluigi = 7
    option_Daisy = 8
    option_Random_Per_Game = 9
    option_Random_Always = 10
    default = 0
    
class ProgTurnsOption(Toggle):
    """Whether the number of turns required to win is a progression item or not."""
    display_name = "Progressive Turns"
    default = False