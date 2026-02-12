from __future__ import annotations
from pprint import pprint

import random
from typing import TYPE_CHECKING, Set
from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from ..boards.aptestworld import watcher as w # import your watcher so it registers its MP3ItemHandler and other logic


if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    
    
# ----------------------------
# Your PartyPlanner shared block
# Lua uses 0x807E0000 virtual, but BizHawk "RDRAM" reads use physical (minus 0x80000000)
# so 0x807E0000 -> 0x007E0000
# ----------------------------
MB_BASE = 0x007D0000

MAGIC_ADDR = MB_BASE + 0x00  # u32 big-endian in your Lua
BOARDINDEX_ADDR = MB_BASE + 0x04  # u32
PLAYER_ADDR = MB_BASE + 0x08 # u8[128] (not used here)

FILLER_COINS_ADDR = MB_BASE + 0xB1 # u8
GIVEN_COINS_ADDR = MB_BASE + 0xB2 # u8

INV_ADDR = 0x007D00C8  # u8[16] (not used here)
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
                "d3" : 0x000CDBD4
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
                "d3" : 0x000CDB20
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
                "d3" : 0x000CDB6C
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
                "d3" : 0x000CDBB8
            }
        }
    }
class MP3ItemHandler():
    def __init__(self, addr, Icode):
        self.addr = addr
        self.ICode = Icode
        self.value = 0
        self.initialized = False
    
    def read(self, ctx: "BizHawkClientContext"):
        value = sum(
            1 for item_id in ctx.items_received if item_id.item == self.ICode
        )
        return value
    
    async def check_and_write(self, ctx: "BizHawkClientContext"):
        new_value = self.read(ctx)
        
        if not self.initialized:
            # First time: set to total value
            self.value = new_value
            self.initialized = True
            if new_value > 0:
                await bizhawk.write(ctx.bizhawk_ctx, [
                    (self.addr, [new_value], "RDRAM"),
                ])
        elif self.value != new_value:
            # Subsequent times: read current and increment
            inv = await bizhawk.read(ctx.bizhawk_ctx, [(self.addr, 1, "RDRAM")])
            current_val = int.from_bytes(inv[0], "big")
            write_val = current_val + (new_value - self.value)
            self.value = new_value
            await bizhawk.write(ctx.bizhawk_ctx, [
                (self.addr, [write_val], "RDRAM"),
            ])
class Watcher:
    def __init__(self):
        self.magic = -1
        self.MPitems = []
        self.board_id = -1
        self.boardWatcher = None
        self.local_checked_locations = set()
        self.last_scene = -1
        self.p1_char = None
        self.c1_char = None
        self.c2_char = None
        self.c3_char = None
    async def update(self, ctx: "BizHawkClientContext"):
        sd = getattr(ctx, "slot_data", None)
        if not sd:
            return
        player_char = sd.get("player_names", 0)
        com1_name = sd.get("com1_names", 0)
        com2_name = sd.get("com2_names", 0)
        com3_name = sd.get("com3_names", 0)
        try:
            reads = await bizhawk.read(ctx.bizhawk_ctx, [
                (MAGIC_ADDR, 4, "RDRAM"),
                (BOARDINDEX_ADDR, 4, "RDRAM"),
                (PLAYER_ADDR, 1, "RDRAM"),
                (global_addrs["player"][0]["controller"], 1, "RDRAM"),
                (global_addrs["player"][1]["controller"], 1, "RDRAM"),
                (global_addrs["player"][2]["controller"], 1, "RDRAM"),
                (global_addrs["player"][3]["controller"], 1, "RDRAM"),
                (global_addrs["player"][0]["char"], 1, "RDRAM"),
                (global_addrs["player"][1]["char"], 1, "RDRAM"),
                (global_addrs["player"][2]["char"], 1, "RDRAM"),
                (global_addrs["player"][3]["char"], 1, "RDRAM"),
                (global_addrs["scene"], 2, "RDRAM"),
            ])
        except bizhawk.RequestFailedError:
            return  # reconnect loop will handle it

        magic = int.from_bytes(reads[0], "big")
        if magic != self.magic or not self.MPitems:
            self.MPitems = []
            for i in range(19):
                item_id = 2 + i
                if i in [5,14, 18]:  # skip keys
                    continue
                self.MPitems.append(MP3ItemHandler(INV_ADDR + i, item_id))
            self.magic = magic
        board_id = int.from_bytes(reads[1], "big")
        if board_id != self.board_id:
            if board_id == 1000:
                self.board_id = board_id
                self.boardWatcher = w.APTBwatcher()
        for i in self.MPitems:
            await i.check_and_write(ctx)
        await self.boardWatcher.update(ctx) if self.boardWatcher else None
        total_coin_items_received = sum(
            1 for item_id in ctx.items_received if item_id.item == 1
        ) * 3
        await bizhawk.write(ctx.bizhawk_ctx, [
            (FILLER_COINS_ADDR, [total_coin_items_received & 0xFF], "RDRAM"),
        ])
        curscene = int.from_bytes(reads[11], "big")
        if curscene == 106: 
            # Chancetime bugfix: if scene is Chancetime, force all CPUs to be a static set of characters to prevent softlock due to game not handling duplicate characters properly in that scene. 
            for i in range(4): 
                await bizhawk.write(ctx.bizhawk_ctx, [
                    (global_addrs["player"][i]["char"], [i], "RDRAM"),
                ])
        if self.last_scene != curscene and curscene in [120 ,83 , 71]:
            for player_num in range(3,7):
                if int.from_bytes(reads[player_num], "big") == 0 and player_char != 0:
                    if (player_char == 9 and curscene == 83) or player_char == 10:
                        self.p1_char = None
                        player_char = random.randint(1,8)
                    if player_char == 9:
                        player_char = self.p1_char if self.p1_char else random.randint(1,8)
                        self.p1_char = player_char
                    await bizhawk.write(ctx.bizhawk_ctx, [
                        (global_addrs["player"][player_num-3]["char"], [player_char-1], "RDRAM"),
                    ])
                elif int.from_bytes(reads[player_num], "big") == 1 and com1_name != 0:
                    if (com1_name == 9 and curscene == 83) or com1_name == 10:
                        self.c1_char = None
                        com1_name = random.randint(1,8)
                    if com1_name == 9:
                        com1_name = self.c1_char if self.c1_char else random.randint(1,8)
                        self.c1_char = com1_name
                    await bizhawk.write(ctx.bizhawk_ctx, [
                        (global_addrs["player"][player_num-3]["char"], [com1_name-1], "RDRAM"),
                    ])
                elif int.from_bytes(reads[player_num], "big") == 2 and com2_name != 0:
                    if (com2_name == 9 and curscene == 83) or com2_name == 10:
                        self.c2_char = None
                        com2_name = random.randint(1,8)
                    if com2_name == 9:
                        com2_name = self.c2_char if self.c2_char else random.randint(1,8)
                        self.c2_char = com2_name
                    await bizhawk.write(ctx.bizhawk_ctx, [
                        (global_addrs["player"][player_num-3]["char"], [com2_name-1], "RDRAM"),
                    ])
                elif int.from_bytes(reads[player_num], "big") == 3 and com3_name != 0:
                    if (com3_name == 9 and curscene == 83) or com3_name == 10:
                        self.c3_char = None
                        com3_name = random.randint(1,8)
                    if com3_name == 9:
                        com3_name = self.c3_char if self.c3_char else random.randint(1,8)
                        self.c3_char = com3_name
                    await bizhawk.write(ctx.bizhawk_ctx, [
                        (global_addrs["player"][player_num-3]["char"], [com3_name-1], "RDRAM"),
                    ])
        self.last_scene = curscene
        pprint(f"Scene changed: {self.last_scene}")