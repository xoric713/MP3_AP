// NAME: Send Zones (MP3)
// GAMES: MP3_USA
// EXECUTION: Direct
// PARAM: Space|SpaceID

#include "ultra64.h"

#define MB_BASE  0x807D0000u
#define MB_MAGIC 0x41504258u  // 'APBX'


typedef volatile struct {
    u32 magic;
    u32 boardIndex;
    u8 Player;
    u8 Spaces[128];
    u8 Zone_1;
    u8 Z1_open;
    u8 Zone_2;
    u8 Z2_open;
    u8 Zone_3;
    u8 Z3_open;
    u8 Zone_4;
    u8 Z4_open;
    u8 Zone_5;
    u8 Z5_open;
    u8 Zone_6;
    u8 Z6_open;
    u8 FillerCoins;
    u8 GivenCoins;
    u8 Shrooment;
} Mailbox;

#define MAILBOX ((Mailbox*)MB_BASE)


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
    if(SID == 5 && MAILBOX->Player == 1 && MAILBOX->Zone_1 == 0){
        MAILBOX->Zone_1 = 1;
    }
    if(SID == 12 && MAILBOX->Player == 1 && MAILBOX->Zone_2 == 0){
        MAILBOX->Zone_2 = 1;
    }
    if(SID == 23 && MAILBOX->Player == 1 && MAILBOX->Zone_3 == 0){
        MAILBOX->Zone_3 = 1;
    }
    if(SID == 42 && MAILBOX->Player == 1 && MAILBOX->Zone_4 == 0){
        MAILBOX->Zone_4 = 1;
    }
    if(SID == 85 && MAILBOX->Player == 1 && MAILBOX->Zone_5 == 0){
        MAILBOX->Zone_5 = 1;
    }
    if(SID == 58 && MAILBOX->Player == 1 && MAILBOX->Zone_6 == 0){
        MAILBOX->Zone_6 = 1;
    }
}
