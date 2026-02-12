from __future__ import annotations

from typing import TYPE_CHECKING, Set
from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
# import your watcher so it registers its MP3ItemHandler and other logic

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
MB_BASE = 0x007D0000

MAGIC_ADDR = MB_BASE + 0x00  # u32 big-endian in your Lua
BOARDINDEX_ADDR = MB_BASE + 0x04  # u32
PLAYER_ADDR = MB_BASE + 0x08 # u8[128] (not used here)
    
SPACE_ARRAY_ADDR = MB_BASE + 0x09 
ZONE1_ADDR = MB_BASE + 0x89 # u8
ZONE2_ADDR = MB_BASE + 0x8A # u8
ZONE3_ADDR = MB_BASE + 0x8B # u8
ZONE4_ADDR = MB_BASE + 0x8C # u8
ZONE5_ADDR = MB_BASE + 0x8D # u8
ZONE6_ADDR = MB_BASE + 0x8E # u8
ZONE7_ADDR = MB_BASE + 0x8F # u8
ZONE8_ADDR = MB_BASE + 0x90 # u8
ZONE9_ADDR = MB_BASE + 0x91 # u8
ZONE10_ADDR = MB_BASE + 0x92 # u8
ZONE11_ADDR = MB_BASE + 0x93 # u8
ZONE12_ADDR = MB_BASE + 0x94 # u8
ZONE13_ADDR = MB_BASE + 0x95 # u8
ZONE14_ADDR = MB_BASE + 0x96 # u8
ZONE15_ADDR = MB_BASE + 0x97 # u8
ZONE16_ADDR = MB_BASE + 0x98 # u8
ZONE17_ADDR = MB_BASE + 0x99 # u8
ZONE18_ADDR = MB_BASE + 0x9A # u8
ZONE19_ADDR = MB_BASE + 0x9B # u8
ZONE20_ADDR = MB_BASE + 0x9C # u8
Z1OPEN_ADDR = MB_BASE + 0x9D # u8
Z2OPEN_ADDR = MB_BASE + 0x9E # u8
Z3OPEN_ADDR = MB_BASE + 0x9F # u8
Z4OPEN_ADDR = MB_BASE + 0xA0 # u8
Z5OPEN_ADDR = MB_BASE + 0xA1 # u8
Z6OPEN_ADDR = MB_BASE + 0xA2 # u8
Z7OPEN_ADDR = MB_BASE + 0xA3 # u8
Z8OPEN_ADDR = MB_BASE + 0xA4 # u8
Z9OPEN_ADDR = MB_BASE + 0xA5 # u8
Z10OPEN_ADDR = MB_BASE + 0xA6 # u8
Z11OPEN_ADDR = MB_BASE + 0xA7 # u8
Z12OPEN_ADDR = MB_BASE + 0xA8 # u8
Z13OPEN_ADDR = MB_BASE + 0xA9 # u8
Z14OPEN_ADDR = MB_BASE + 0xAA # u8
Z15OPEN_ADDR = MB_BASE + 0xAB # u8
Z16OPEN_ADDR = MB_BASE + 0xAC # u8
Z17OPEN_ADDR = MB_BASE + 0xAD # u8
Z18OPEN_ADDR = MB_BASE + 0xAE # u8
Z19OPEN_ADDR = MB_BASE + 0xAF # u8
Z20OPEN_ADDR = MB_BASE + 0xB0 # u8
SHROOMENT_ADDR = MB_BASE + 0xB3  # u8
global_addrs = {
        "scene" : 0x000CE202,
        "total_turns" : 0x000CD05A,
        "current_turn" : 0x000CD05B,
        "player" : {
            0 : {
                "cpu_diff" : 0x000D1109,
                "controller" : 0x000D110A,
                "char" : 0x000D110B,
                "coins" : 0x000D1112, # u16
                "stars" : 0x000D1116,
                "turn_color" : 0x000D1124,
                "d1" : 0x000CDBD2,
                "d2" : 0x000CDBD3,
                "d3" : 0x000CDBD4,
                "position" : SHROOMENT_ADDR+1
            },
            1 : {
                "cpu_diff" : 0x000D1141,
                "controller" : 0x000D1142,
                "char" : 0x000D1143,
                "coins" : 0x000D114A, # u16
                "stars" : 0x000D114E,
                "turn_color" : 0x000D115C,
                "d1" : 0x000CDB1E,
                "d2" : 0x000CDB1F,
                "d3" : 0x000CDB20,
                "position" : SHROOMENT_ADDR+2
            },
            2 : {
                "cpu_diff" : 0x000D1179,
                "controller" : 0x000D117A,
                "char" : 0x000D117B,
                "coins" : 0x000D1182, # u16
                "stars" : 0x000D1186,
                "turn_color" : 0x000D1194,
                "d1" : 0x000CDB6A,
                "d2" : 0x000CDB6B,
                "d3" : 0x000CDB6C,
                "position" : SHROOMENT_ADDR+3
            },
            3 : {
                "cpu_diff" : 0x000D11B1,
                "controller" : 0x000D11B2,
                "char" : 0x000D11B3,
                "coins" : 0x000D11BA, # u16
                "stars" : 0x000D11BE,
                "turn_color" : 0x000D11CC,
                "d1" : 0x000CDBB6,
                "d2" : 0x000CDBB7,
                "d3" : 0x000CDBB8,
                "position" : SHROOMENT_ADDR+4
            }
        }
    }
class APTBwatcher:
    def __init__(self):
        self.last_turn = 1
        self.local_checked_locations = set()
    async def update(self, ctx: "BizHawkClientContext"):
        sd = getattr(ctx, "slot_data", None)
        if sd is None:
            return  # will be set on next tick, ignore for now

        try:
            reads = await bizhawk.read(ctx.bizhawk_ctx, [
                    (ZONE1_ADDR, 1, "RDRAM"),
                    (Z1OPEN_ADDR, 1, "RDRAM"),
                    (ZONE2_ADDR, 1, "RDRAM"),
                    (Z2OPEN_ADDR, 1, "RDRAM"),
                    (ZONE3_ADDR, 1, "RDRAM"),
                    (Z3OPEN_ADDR, 1, "RDRAM"),
                    (ZONE4_ADDR, 1, "RDRAM"),
                    (Z4OPEN_ADDR, 1, "RDRAM"),
                    (ZONE5_ADDR, 1, "RDRAM"),
                    (Z5OPEN_ADDR, 1, "RDRAM"),
                    (ZONE6_ADDR, 1, "RDRAM"),
                    (Z6OPEN_ADDR, 1, "RDRAM"),
                    (SHROOMENT_ADDR, 1, "RDRAM"),
                    (BOARDINDEX_ADDR, 4, "RDRAM"),
                    (global_addrs["current_turn"], 1, "RDRAM"),
                    (global_addrs["player"][0]["position"], 1, "RDRAM"),
                    (global_addrs["player"][1]["position"], 1, "RDRAM"),
                    (global_addrs["player"][2]["position"], 1, "RDRAM"),
                    (global_addrs["player"][3]["position"], 1, "RDRAM"),
                    (global_addrs["player"][0]["controller"], 1, "RDRAM"),
                    (global_addrs["player"][1]["controller"], 1, "RDRAM"),
                    (global_addrs["player"][2]["controller"], 1, "RDRAM"),
                    (global_addrs["player"][3]["controller"], 1, "RDRAM"),
                ])
            spaces = await bizhawk.read(ctx.bizhawk_ctx, [
                    (SPACE_ARRAY_ADDR + i, 1, "RDRAM") for i in range(128)
                ])
        except bizhawk.RequestFailedError:
            return  # reconnect loop will handle it
    
        z0_flags = []
        cnt = 0
        while cnt < 7:
            temp = spaces.pop(0)
            z0_flags.append(int.from_bytes(temp, "big"))
            cnt += 1
        z0_flags.append(int.from_bytes(reads[0], "big"))  # only 7 bits used
        z1_open = int.from_bytes(reads[1], "big")  # 1 byte
        z1_flags = []
        cnt = 0
        while cnt < 7:
            temp = spaces.pop(0)
            z1_flags.append(int.from_bytes(temp, "big"))
            cnt += 1
        z1_flags.append(int.from_bytes(reads[2], "big"))  # only 7 bits used
        z2_open = int.from_bytes(reads[3], "big")  #
        z2_flags = []
        cnt = 0
        while cnt < 7:
            temp = spaces.pop(0)
            z2_flags.append(int.from_bytes(temp, "big"))
            cnt += 1
        z2_flags.append(int.from_bytes(reads[4], "big"))  # only 7 bits used
        z3_open = int.from_bytes(reads[5], "big")  #
        z3_flags = []
        cnt = 0
        while cnt < 18:
            temp = spaces.pop(0)
            z3_flags.append(int.from_bytes(temp, "big"))
            cnt += 1
        z3_flags.append(int.from_bytes(reads[6], "big"))  # only 2 bits used
        z4_open = int.from_bytes(reads[7], "big")  #
        z4_flags = []
        cnt = 0
        while cnt < 20:
            temp = spaces.pop(0)
            z4_flags.append(int.from_bytes(temp, "big"))
            cnt += 1
        z4_flags.append(int.from_bytes(reads[8], "big"))  # only 4 bits used
        z5_open = int.from_bytes(reads[9], "big")  #
        z5_flags = []
        cnt = 0
        while cnt < 6:
            temp = spaces.pop(0)
            z5_flags.append(int.from_bytes(temp, "big"))
            cnt += 1
        z5_flags.append(int.from_bytes(reads[10], "big"))  # only 6 bits used
        z6_open = int.from_bytes(reads[11], "big")  #
        z6_flags = []
        cnt = 0
        while cnt < 13:
            temp = spaces.pop(0)
            z6_flags.append(int.from_bytes(temp, "big"))
            cnt += 1
        shrooment = int.from_bytes(reads[12], "big")  
        
        board_id = int.from_bytes(reads[13], "big")
        turncount = sd.get("ap_test_board_turn_count", 0)
        progturns = sd.get("progturns", 0)
        W_Watch = sum(
            1 for item_id in ctx.items_received if item_id.item == board_id + 9
        ) * 5
        await bizhawk.write(ctx.bizhawk_ctx, [(global_addrs["total_turns"], [turncount], "RDRAM")])
        if progturns:
            progturn = sum(
            1 for item_id in ctx.items_received if item_id.item == board_id + 8
            )
            if int.from_bytes(reads[14], "big") > progturn + 1:
                await bizhawk.write(ctx.bizhawk_ctx, [(global_addrs["current_turn"], [progturn+1], "RDRAM")])
        curturn = int.from_bytes(reads[14], "big")
        max = 5 + W_Watch
        if progturns:
            if max > progturn + 1:
                max = progturn + 1
        await bizhawk.write(ctx.bizhawk_ctx, [(MB_BASE - 0x01, [max], "RDRAM")])
        locs_to_send = {board_id + i for i, val in enumerate(z0_flags, start = 1) if val != 0}
        locs_to_send.update({board_id + i + 8 for i, val in enumerate(z1_flags, start = 1) if val != 0})
        locs_to_send.update({board_id + i + 16 for i, val in enumerate(z2_flags, start = 1) if val != 0})
        locs_to_send.update({board_id + i + 24 for i, val in enumerate(z3_flags, start = 1) if val != 0})
        locs_to_send.update({board_id + i + 43 for i, val in enumerate(z4_flags, start = 1) if val != 0})
        locs_to_send.update({board_id + i + 65 for i, val in enumerate(z5_flags, start = 1) if val != 0})
        locs_to_send.update({board_id + i + 71 for i, val in enumerate(z6_flags, start = 1) if val != 0})
        player_position = -1
        for i in range(4):
            controller = int.from_bytes(reads[19+i], "big")
            if controller == 0 and self.last_turn != curturn:
                player_position = int.from_bytes(reads[15+i], "big")
                if player_position == 0: 
                    locs_to_send.add(board_id + 85 + self.last_turn) # first place this turn
                self.last_turn = curturn
        if locs_to_send != self.local_checked_locations:
            self.local_checked_locations = locs_to_send
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": list(locs_to_send),
            }])
            
        
        shrooment_count = sum(
            1 for item_id in ctx.items_received if item_id.item == board_id + 7
        )
        if shrooment != shrooment_count:
            await bizhawk.write(ctx.bizhawk_ctx, [
                (SHROOMENT_ADDR, [shrooment_count], "RDRAM"),
            ])
        
        has_key_1 = any(
            item_id.item == board_id + 1 for item_id in ctx.items_received
        )
        if has_key_1 and z1_open == 0:
            await bizhawk.write(ctx.bizhawk_ctx, [
                (Z1OPEN_ADDR, [1], "RDRAM"),
            ])
        has_key_2 = any(
            item_id.item == board_id + 2 for item_id in ctx.items_received
        )
        if has_key_2 and z2_open == 0:
            await bizhawk.write(ctx.bizhawk_ctx, [
                (Z2OPEN_ADDR, [1], "RDRAM"),
            ])
        has_key_3 = any(
            item_id.item == board_id + 3 for item_id in ctx.items_received
        )
        if has_key_3 and z3_open == 0:
            await bizhawk.write(ctx.bizhawk_ctx, [
                (Z3OPEN_ADDR, [1], "RDRAM"),
            ])
        has_key_4 = any(
            item_id.item == board_id + 4 for item_id in ctx.items_received
        )
        if has_key_4 and z4_open == 0:
            await bizhawk.write(ctx.bizhawk_ctx, [
                (Z4OPEN_ADDR, [1], "RDRAM"),
            ])
        has_key_5 = any(
            item_id.item == board_id + 5 for item_id in ctx.items_received
        )
        if has_key_5 and z5_open == 0:
            await bizhawk.write(ctx.bizhawk_ctx, [
                (Z5OPEN_ADDR, [1], "RDRAM"),
            ])
        has_key_6 = any(
            item_id.item == board_id + 6 for item_id in ctx.items_received
        )
        if has_key_6 and z6_open == 0:
                await bizhawk.write(ctx.bizhawk_ctx, [
                    (Z6OPEN_ADDR, [1], "RDRAM"),
                ])
        SS = sum(
            item_id.item == board_id + 8 for item_id in ctx.items_received
        )
        if SS > turncount and board_id != 0:
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL,
            }])