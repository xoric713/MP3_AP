// NAME: get positions
// GAMES: MP3_USA
// EXECUTION: Direct

#include "ultra64.h"
#define MB_BASE  0x807D0000u
#define MB_MAGIC 0x41504258u  // 'APBX'
typedef volatile struct {
    u32 magic;
    u32 boardIndex;
    u8 Player;
    u8 Spaces[128];
    u8 Zones[20];
    u8 Zones_open[20];
    u8 FillerCoins;
    u8 GivenCoins;
    u8 Shrooment;
    u8 positions[4];
} Mailbox;



#define MAILBOX ((Mailbox*)MB_BASE)

#define SANDBOX_BASE 0x807D00C8u

typedef volatile struct {
    u8 inventory[20];
    char text[1000];
    char text2[1000];
    u8 page;
    u8 map[15];
    u8 map2[15];
    u8 flag;
} Box;

#define SANDBOX ((Box*)SANDBOX_BASE)

void main() {
    int i = 0;
    while(i<4){
        MAILBOX->positions[i] = GetPlayerPlacementAtEndOfGame(i);
        i++;
    }
}