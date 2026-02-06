// NAME: Check AP Table (MP3)
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

#define SANDBOX_BASE 0x807E0000u

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
    if (MAILBOX->magic != MB_MAGIC) {
        // mailbox got clobbered — reinit
        MAILBOX->magic = MB_MAGIC;
        MAILBOX->boardIndex = 1000;
        MAILBOX->Player = 0;
        MAILBOX->Zone_1 = 0;
        MAILBOX->Zone_2 = 0;
        MAILBOX->Zone_3 = 0;
        MAILBOX->Zone_4 = 0;
        MAILBOX->Zone_5 = 0;
        MAILBOX->Zone_6 = 0;
        MAILBOX->GivenCoins = 0;
        MAILBOX->Shrooment = 0;

        int i;
        for (i = 0; i < 128; i++) {
            MAILBOX->Spaces[i] = 0;
        }
        // optional: set a “clobbered counter” somewhere in mailbox
    }

    s16 p = GetCurrentPlayerIndex();
    if (PlayerIsCPU(p) != 0) {
        MAILBOX->Player = 0;
    } else {
        MAILBOX->Player = 1;
    }
    // normal operation
    if(MAILBOX->Z1_open == 1 && MAILBOX->Player == 1){
        char *text = "Zone 1 is now open"
        "\xC2"
        "\xFF";
        ShowMessage(-1, text, 0, 0, 0, 0, 0);
        MAILBOX->Z1_open = 2;

        func_800EC9DC();
        CloseMessage();
        func_800EC6EC();

    }
    if(MAILBOX->Z2_open == 1 && MAILBOX->Player == 1){
        char *text = "Zone 2 is now open"
        "\xC2"
        "\xFF";
        ShowMessage(-1, text, 0, 0, 0, 0, 0);
        MAILBOX->Z2_open = 2;

        func_800EC9DC();
        CloseMessage();
        func_800EC6EC();

    }
    if(MAILBOX->Z3_open == 1 && MAILBOX->Player == 1){
        char *text = "Zone 3 is now open"
        "\xC2"
        "\xFF";
        ShowMessage(-1, text, 0, 0, 0, 0, 0);
        MAILBOX->Z3_open = 2;

        func_800EC9DC();
        CloseMessage();
        func_800EC6EC();

    }
    if(MAILBOX->Z4_open == 1 && MAILBOX->Player == 1){
        char *text = "Zone 4 is now open"
        "\xC2"
        "\xFF";
        ShowMessage(-1, text, 0, 0, 0, 0, 0);
        MAILBOX->Z4_open = 2;

        func_800EC9DC();
        CloseMessage();
        func_800EC6EC();

    }
    if(MAILBOX->Z5_open == 1 && MAILBOX->Player == 1){
        char *text = "Zone 5 is now open"
        "\xC2"
        "\xFF";
        ShowMessage(-1, text, 0, 0, 0, 0, 0);
        MAILBOX->Z5_open = 2;

        func_800EC9DC();
        CloseMessage();
        func_800EC6EC();

    }
    if(MAILBOX->Z6_open == 1 && MAILBOX->Player == 1){
        char *text = "Zone 6 is now open"
        "\xC2"
        "\xFF";
        ShowMessage(-1, text, 0, 0, 0, 0, 0);
        MAILBOX->Z6_open = 2;

        func_800EC9DC();
        CloseMessage();
        func_800EC6EC();

    }
    if(MAILBOX->FillerCoins > MAILBOX->GivenCoins && MAILBOX->Player == 1){
        u8 coinsToGive = MAILBOX->FillerCoins - MAILBOX->GivenCoins;
        MAILBOX->GivenCoins = MAILBOX->FillerCoins;
        AdjustPlayerCoinsGradual(p, coinsToGive);
        ShowPlayerCoinChange(p, coinsToGive);
        SleepProcess(30);
    }
        
    enum item {
        ITEM_NONE = 0xFF,
        ITEM_MUSHROOM = 0x00,
        ITEM_SKELETON_KEY = 0x01,
        ITEM_POISON_MUSHROOM = 0x02,
        ITEM_REVERSE_MUSHROOM = 0x03,
        ITEM_CELLULAR_SHOPPER = 0x04,
        ITEM_WARP_BLOCK = 0x05,
        ITEM_PLUNDER_CHEST = 0x06,
        ITEM_BOWSER_PHONE = 0x07,
        ITEM_DUELING_GLOVE = 0x08,
        ITEM_LUCKY_LAMP = 0x09,
        ITEM_GOLDEN_MUSHROOM = 0x0A,
        ITEM_BOO_BELL = 0x0B,
        ITEM_BOO_REPELLANT = 0x0C,
        ITEM_BOWSER_SUIT = 0x0D,
        ITEM_MAGIC_LAMP = 0x0E,
        ITEM_KOOPA_CARD = 0x0F,
        ITEM_BARTER_BOX = 0x10,
        ITEM_LUCKY_COIN = 0x11,
        ITEM_WACKY_WATCH = 0x12
    };

    struct player {
        s8 unk0;
        s8 cpu_difficulty;
        s8 controller;
        u8 character;
        /**
         * Miscellaneous flags.
         * 1: Is CPU player
         */
        u8 flags;
        s8 pad0[5];
        /**
         * Current coin count.
         */
        s16 coins; // 10
        /**
         * Coins obtained during a Mini-Game.
         */
        s16 minigame_coins; // 12
        s8 stars; // 14

        u8 cur_chain_index; // 15
        u8 cur_space_index; // 16
        u8 next_chain_index; // 17
        u8 next_space_index; // 18
        u8 unk1_chain_index; // 19
        u8 unk1_space_index; // 20
        u8 reverse_chain_index; // 21
        u8 reverse_space_index; // 22

        u8 flags2; // 23
        u8 items[3]; // 24
        u8 bowser_suit_flag; // 27
        u8 turn_color_status; // 28

        s8 pad1[7]; // 29 - 35

        void *obj; // 36 // struct object *
        s16 minigame_star; // 40
        s16 coin_star; // 42
        s8 happening_space_count; // 44
        s8 red_space_count;
        s8 blue_space_count;
        s8 chance_space_count;
        s8 bowser_space_count; // 48
        s8 battle_space_count;
        s8 item_space_count;
        s8 bank_space_count;
        s8 game_guy_space_count; // 52

        // s8 pad2[3];
    }; // sizeof == 56
        
    extern struct player *GetPlayerStruct(s32 player_index);
    
    int ItemChosen = 0;
    struct player *player = GetPlayerStruct(p);
    int C = 0;
    while(C<3){
        if(player->items[C] == ITEM_WARP_BLOCK){    
            int k = 0;
            while(k < 90){
                int r = GetRandomByte()%19;
                player->items[C] = r;
                RefreshHUD(p);
                SleepVProcess();
                k++;
            }
            while(player->items[C] == ITEM_WARP_BLOCK){
                int r = GetRandomByte()%19;
                player->items[C] = r;
                RefreshHUD(p);
                SleepVProcess();
                k++;
            }
        }
        C++;
    }
    if(MAILBOX->Player == 1){
        C = 0;
        int k = 0;
        while(C<3){
            if(player->items[C] == ITEM_WARP_BLOCK || player->items[C] == ITEM_MAGIC_LAMP){    
                int k = 0;
                while(k < 90){
                    int r = GetRandomByte()%19;
                    player->items[C] = r;
                    RefreshHUD(p);
                    SleepVProcess();
                    k++;
                }
                while(player->items[C] == ITEM_WARP_BLOCK || player->items[C] == ITEM_MAGIC_LAMP){
                    int r = GetRandomByte()%19;
                    player->items[C] = r;
                    RefreshHUD(p);
                    SleepVProcess();
                    k++;
                }
            }
            SleepProcess(10);
            if(player->items[C] != ITEM_NONE){
                SANDBOX->inventory[player->items[C]] = SANDBOX->inventory[player->items[C]] + 1;
                player->items[C] = ITEM_NONE;
                RefreshHUD(p);
                SleepVProcess();
            }
            C++;
        }
        if(MAILBOX->Shrooment == 1){
            SANDBOX->inventory[ITEM_MUSHROOM] = SANDBOX->inventory[ITEM_MUSHROOM] + 1;
            SleepVProcess();
        }else if(MAILBOX->Shrooment == 2){
            SANDBOX->inventory[ITEM_GOLDEN_MUSHROOM] = SANDBOX->inventory[ITEM_GOLDEN_MUSHROOM] + 1;
            SleepVProcess();
        }
        SANDBOX->page = 0;
        
        while (!ItemChosen && MAILBOX->Player == 1 && SANDBOX->map[0] != 0xFF && SANDBOX->map[0] != 0xFC) {
            SANDBOX->text[0] = '\0';
            char *text = "\x0B"
            "\x1A\x1A\x1A\x1A"
            "Archipelago Inventory Menu"
            "\xC2"
            "\x0A"
            "\x1A\x1A\x1A\x1A"
            "Page ";
            char result[512];
            sprintf(result, "%s%d", text, SANDBOX->page+1);
            char *item_text = "\x0A"
                            "\x1A\x1A\x1A\x1A"
                            "\x0C";
            char *N_P;
            int box;
            for (int i = 0; i < 15; i++){
                if(SANDBOX->page == 0){
                    box = SANDBOX->map[i];
                    N_P = "Next Page";
                }else{
                    box = SANDBOX->map2[i];
                    N_P = "Previous Page";
                }
                
                char buffer[512];
                switch(box){
                    case ITEM_MUSHROOM:
                        sprintf(buffer, "%s%s%d%s", item_text, "Mushroom x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    case ITEM_SKELETON_KEY:
                        sprintf(buffer, "%s%s%d%s", item_text, "Skeleton Key x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    case ITEM_POISON_MUSHROOM:
                        sprintf(buffer, "%s%s%d%s", item_text, "Poison Mushroom x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    case ITEM_REVERSE_MUSHROOM:
                        sprintf(buffer, "%s%s%d%s", item_text, "Reverse Mushroom x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    case ITEM_CELLULAR_SHOPPER:
                        sprintf(buffer, "%s%s%d%s", item_text, "Cellular Shopper x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    case ITEM_WARP_BLOCK:
                        sprintf(buffer, "%s%s%d%s", item_text, "Warp Block x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    // Add cases for other items as needed
                    case ITEM_PLUNDER_CHEST:
                        sprintf(buffer, "%s%s%d%s", item_text, "Plunder Chest x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    case ITEM_BOWSER_PHONE:
                        sprintf(buffer, "%s%s%d%s", item_text, "Bowser Phone x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    case ITEM_DUELING_GLOVE:
                        sprintf(buffer, "%s%s%d%s", item_text, "Dueling Glove x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    case ITEM_LUCKY_LAMP:
                        sprintf(buffer, "%s%s%d%s", item_text, "Lucky Lamp x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    case ITEM_GOLDEN_MUSHROOM:
                        sprintf(buffer, "%s%s%d%s", item_text, "Golden Mushroom x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    case ITEM_BOO_BELL:
                        sprintf(buffer, "%s%s%d%s", item_text, "Boo Bell x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    case ITEM_BOO_REPELLANT:
                        sprintf(buffer, "%s%s%d%s", item_text, "Boo Repellant x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    case ITEM_BOWSER_SUIT:
                        sprintf(buffer, "%s%s%d%s", item_text, "Bowser Suit x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    case ITEM_MAGIC_LAMP:
                        sprintf(buffer, "%s%s%d%s", item_text, "Magic Lamp x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    case ITEM_KOOPA_CARD:
                        sprintf(buffer, "%s%s%d%s", item_text, "Koopa Card x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    case ITEM_BARTER_BOX:
                        sprintf(buffer, "%s%s%d%s", item_text, "Barter Box x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    case ITEM_LUCKY_COIN:
                        sprintf(buffer, "%s%s%d%s", item_text, "Lucky Coin x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    case ITEM_WACKY_WATCH:
                        sprintf(buffer, "%s%s%d%s", item_text, "Wacky Watch x ", SANDBOX->inventory[box], "\x0D");
                        break;
                    case 0xFD:
                        sprintf(buffer, "%s%s%s", item_text, N_P, "\x0D");
                        break;
                    case 0xFE:
                        sprintf(buffer, "%s%s%s", item_text, "View Map", "\x0D");
                        break;
                    case 0xFF:
                        sprintf(buffer, "%s%s%s", item_text, "Close Menu", "\x0D");
                        break;
                    case 0xFC:
                        sprintf(buffer, "%s", "");
                        break;
                }
                append_string(SANDBOX->text, buffer);
            }
            sprintf(SANDBOX->text2, "%s%s", result, SANDBOX->text);
            
            ShowMessage(0x16, SANDBOX->text2, 0, 0, 0, 0, 0);
            s32 choice = GetBasicPromptSelection(player->controller, 0);
            // Obligatory message box closing/cleanup calls.
            CloseMessage();
            func_800EC6EC();
            if(SANDBOX->page == 0){
                if(SANDBOX->map[choice] == 0xFF){
                    ItemChosen = 1;
                }else if(SANDBOX->map[choice] == 0xFE){
                    ViewBoardMap();
                }else if(SANDBOX->map[choice] == 0xFD){
                    SANDBOX->page = 1;
                }else{
                    player->items[0] = SANDBOX->map[choice];
                    SANDBOX->inventory[SANDBOX->map[choice]] = SANDBOX->inventory[SANDBOX->map[choice]] - 1;
                    ItemChosen = 1; 
                }
            }else{
                if(SANDBOX->map2[choice] == 0xFF){
                    ItemChosen = 1;
                }else if(SANDBOX->map2[choice] == 0xFE){
                    ViewBoardMap();
                }else if(SANDBOX->map2[choice] == 0xFD){
                    SANDBOX->page = 0;
                }else{
                    player->items[0] = SANDBOX->map2[choice];
                    SANDBOX->inventory[SANDBOX->map2[choice]] = SANDBOX->inventory[SANDBOX->map2[choice]] - 1;
                    ItemChosen = 1;
                } 
            }
        }
    }   
}

void append_string(char* dest, const char* src) {
    while (*dest) {
        dest++;
    }
    while (*src) {
        *dest++ = *src++;
    }
    *dest = '\0';
}


