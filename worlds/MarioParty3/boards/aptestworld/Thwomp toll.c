// NAME: Thwomp Toll (MP3)
// GAMES: MP3_USA
// EXECUTION: Direct
// PARAM: +Number|ZONE
// PARAM: Space|DECLINE_DEST

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

void main() {
    char text[12];
    int_to_str(ZONE, text);
    char *ThwompNo_Message =
        "\x1A\x1A\x1A\x1A" // Standard padding for picture
        "No passing for you until you have Zone "
        "\x11" 
        "\xC2" // !
        "\xFF";
    int *chk = 0;
    if (ZONE == 1 && MAILBOX->Z1_open < 2) {
        chk = 1;
    }
    if (ZONE == 2 && MAILBOX->Z2_open < 2) {
        chk = 1;
    }
    if (ZONE == 3 && MAILBOX->Z3_open < 2) {
        chk = 1;
    }
    if (ZONE == 4 && MAILBOX->Z4_open < 2) {
        chk = 1;
    }
    if (ZONE == 5 && MAILBOX->Z5_open < 2) {
        chk = 1;
    }
    if (ZONE == 6 && MAILBOX->Z6_open < 2) {
        chk = 1;
    }
    if (MAILBOX->Player == 1 && chk != 0) {
        SetBoardPlayerAnimation(-1, -1, 2);
        PlaySound(0x1AE); // Thwomp sound
        ShowMessage(8, ThwompNo_Message, text, 0, 0, 0, 0);
        func_800EC9DC();
        CloseMessage();
        func_800EC6EC();

        SetNextChainAndSpace(
            -1,
            DECLINE_DEST_chain_index,
            DECLINE_DEST_chain_space_index
        );
        return;
    }

}


