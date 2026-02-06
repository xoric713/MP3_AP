// NAME: give to bank
// GAMES: MP3_USA
// EXECUTION: Direct

#include "ultra64.h"
#define BANK (*(unsigned short*)0x800CD0B4)

extern s16 GetCurrentPlayerIndex();
void main() {
    
    s16 p = GetCurrentPlayerIndex();
    AdjustPlayerCoinsGradual(p, -5);
    ShowPlayerCoinChange(p, -5);
    BANK +=5;
}