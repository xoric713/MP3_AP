// NAME: Send Space (MP3)
// GAMES: MP3_USA
// EXECUTION: Direct
// PARAM: +Number|SpaceID

#include "ultra64.h"

#define MB_BASE  0x807D0000u
#define MB_MAGIC 0x41504258u  // 'APBX'


typedef volatile struct {
    u32 magic;
    u32 boardIndex;
    u8 Player;
    u8 Spaces[128];
    u8 Zone[20];
    u8 Zopen[20];
    u8 FillerCoins;
    u8 GivenCoins;
    u8 Shrooment;
    u8 positions[4];
} Mailbox;

#define MAILBOX ((Mailbox*)MB_BASE)
#define BANK (*(unsigned short*)0x800CD0B4)


extern s16 GetCurrentPlayerIndex();
extern u32 PlayerIsCPU(s16 index);

void int_to_str(int value, char* buf) {
    char temp[12];
    int i = 0, j = 0;

    if (value == 0) {
        buf[0] = '0';
        buf[1] = 0;
        return;
    }

    while (value > 0) {
        temp[i++] = '0' + (value % 10);
        value /= 10;
    }

    while (i > 0) {
        buf[j++] = temp[--i];
    }

    buf[j] = 0;
}


void main()
{
    u8 SID = SpaceID;
    if(MAILBOX->Player == 1 && MAILBOX->Spaces[SID-1] == 0){
        MAILBOX->Spaces[SID-1] = 1;
    }
}