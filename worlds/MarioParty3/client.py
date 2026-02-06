from __future__ import annotations

from typing import TYPE_CHECKING, Set
from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient


if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


# ----------------------------
# ROM validation (N64 header)
# ----------------------------
ROM_TITLE_OFFSET = 0x20
ROM_TITLE_LEN = 0x14  # 20 bytes, ASCII, space padded

EXPECTED_TITLE = "MarioParty3"  # what your ROM header shows


# ----------------------------
# Your PartyPlanner shared block
# Lua uses 0x807E0000 virtual, but BizHawk "RDRAM" reads use physical (minus 0x80000000)
# so 0x807E0000 -> 0x007E0000
# ----------------------------
MB_BASE = 0x007D0000

MAGIC_ADDR = MB_BASE + 0x00  # u32 big-endian in your Lua
BOARDINDEX_ADDR = MB_BASE + 0x04  # u32
PLAYER_ADDR = MB_BASE + 0x08
SPACE_ARRAY_ADDR = MB_BASE + 0x09  # u8[128] (not used here)
ZONE1_ADDR = MB_BASE + 0x89 # u8
Z1OPEN_ADDR = MB_BASE + 0x8A # u8
ZONE2_ADDR = MB_BASE + 0x8B # u8
Z2OPEN_ADDR = MB_BASE + 0x8C # u8
ZONE3_ADDR = MB_BASE + 0x8D # u8
Z3OPEN_ADDR = MB_BASE + 0x8E # u8
ZONE4_ADDR = MB_BASE + 0x8F # u8
Z4OPEN_ADDR = MB_BASE + 0x90 # u8
ZONE5_ADDR = MB_BASE + 0x91 # u8
Z5OPEN_ADDR = MB_BASE + 0x92 # u8
ZONE6_ADDR = MB_BASE + 0x93 # u8
Z6OPEN_ADDR = MB_BASE + 0x94 # u8
FILLER_COINS_ADDR = MB_BASE + 0x95 # u8
GIVEN_COINS_ADDR = MB_BASE + 0x96 # u8
SHROOMENT_ADDR = MB_BASE + 0x97  # u8

INV_ADDR = 0x007E0000  # u8[16] (not used here)

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


class MarioParty3Client(BizHawkClient):
    # MUST match your World.game string in world.py
    game = "Mario Party 3"
    system = "N64"

    # You are not using AP-generated patch files, so this can be omitted.
    # But leaving it defined is harmless; generic launcher uses it for display/patch workflows.
    patch_suffix = ".apmp3"

    local_checked_locations: Set[int]

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.magic = -1
        self.MPitems = []

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        """
        This is what makes the generic BizHawk client say:
        'Running handler for Mario Party 3'
        instead of 'no handler was found'.
        """
        from CommonClient import logger

        try:
            raw = await bizhawk.read(ctx.bizhawk_ctx, [(ROM_TITLE_OFFSET, ROM_TITLE_LEN, "ROM")])
            title = raw[0].decode("ascii", errors="ignore").rstrip(" \0")
        except bizhawk.RequestFailedError:
            return False  # will retry next tick

        if title != EXPECTED_TITLE:
            return False

        # If you want: wait until a PartyPlanner/AP board is actually injected before going "ready"
        # (Optional: you can return True immediately if you prefer the handler to attach as soon as MP3 ROM is loaded.)
        try:
            magic_bytes = await bizhawk.read(ctx.bizhawk_ctx, [(MAGIC_ADDR, 4, "RDRAM")])
            self.magic = int.from_bytes(magic_bytes[0], "big")
        except bizhawk.RequestFailedError:
            return False

        if self.magic == 0:
            logger.info("Mario Party 3 detected. Waiting for PartyPlanner/AP board (MAGIC not set yet).")
            # Returning True here is OK too — it just means your watcher has to no-op until MAGIC shows up.
            # If you return False, the client may keep 'searching' for a handler depending on its flow.
            # I recommend TRUE so it attaches immediately once MP3 is loaded.
            # We'll attach immediately:

        ctx.game = self.game
        ctx.items_handling = 0b011  # receive items (typical)
        ctx.want_slot_data = False
        ctx.watcher_timeout = 0.125  # how often the watcher ticks

        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        """
        Main loop:
        - Read your shared memory block
        - Convert it into LocationChecks / Goal / etc
        - Write received items into your shared block for Lua to apply
        """
        from CommonClient import logger
        try:
            reads = await bizhawk.read(ctx.bizhawk_ctx, [
                (MAGIC_ADDR, 4, "RDRAM"),
                (BOARDINDEX_ADDR, 4, "RDRAM"),
                (PLAYER_ADDR, 1, "RDRAM"),
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
            ])
            spaces = await bizhawk.read(ctx.bizhawk_ctx, [
                (SPACE_ARRAY_ADDR + i, 1, "RDRAM") for i in range(128)
            ])
        except bizhawk.RequestFailedError:
            return  # reconnect loop will handle it

        magic = int.from_bytes(reads[0], "big")
        if magic != self.magic or not self.MPitems:
            self.MPitems = []
            for i in range(19):
                item_id = 2 + i
                if i in [5,14]:  # skip keys
                    continue
                self.MPitems.append(MP3ItemHandler(INV_ADDR + i, item_id))
            self.magic = magic
        for i in self.MPitems:
            await i.check_and_write(ctx)
        z0_flags = []
        cnt = 0
        while cnt < 7:
            temp = spaces.pop(0)
            z0_flags.append(int.from_bytes(temp, "big"))
            cnt += 1
        z0_flags.append(int.from_bytes(reads[3], "big"))  # only 7 bits used
        z1_open = int.from_bytes(reads[4], "big")  # 1 byte
        z1_flags = []
        cnt = 0
        while cnt < 7:
            temp = spaces.pop(0)
            z1_flags.append(int.from_bytes(temp, "big"))
            cnt += 1
        z1_flags.append(int.from_bytes(reads[5], "big"))  # only 7 bits used
        z2_open = int.from_bytes(reads[6], "big")  #
        z2_flags = []
        cnt = 0
        while cnt < 7:
            temp = spaces.pop(0)
            z2_flags.append(int.from_bytes(temp, "big"))
            cnt += 1
        z2_flags.append(int.from_bytes(reads[7], "big"))  # only 7 bits used
        z3_open = int.from_bytes(reads[8], "big")  #
        z3_flags = []
        cnt = 0
        while cnt < 18:
            temp = spaces.pop(0)
            z3_flags.append(int.from_bytes(temp, "big"))
            cnt += 1
        z3_flags.append(int.from_bytes(reads[9], "big"))  # only 2 bits used
        z4_open = int.from_bytes(reads[10], "big")  #
        z4_flags = []
        cnt = 0
        while cnt < 20:
            temp = spaces.pop(0)
            z4_flags.append(int.from_bytes(temp, "big"))
            cnt += 1
        z4_flags.append(int.from_bytes(reads[11], "big"))  # only 4 bits used
        z5_open = int.from_bytes(reads[12], "big")  #
        z5_flags = []
        cnt = 0
        while cnt < 6:
            temp = spaces.pop(0)
            z5_flags.append(int.from_bytes(temp, "big"))
            cnt += 1
        z5_flags.append(int.from_bytes(reads[13], "big"))  # only 6 bits used
        z6_open = int.from_bytes(reads[14], "big")  #
        z6_flags = []
        cnt = 0
        while cnt < 13:
            temp = spaces.pop(0)
            z6_flags.append(int.from_bytes(temp, "big"))
            cnt += 1
        shrooment = int.from_bytes(reads[15], "big")  #
        
        board_id = int.from_bytes(reads[1], "big")
        locs_to_send = {board_id + i for i, val in enumerate(z0_flags, start = 1) if val != 0}
        locs_to_send.update({board_id + i + 8 for i, val in enumerate(z1_flags, start = 1) if val != 0})
        locs_to_send.update({board_id + i + 16 for i, val in enumerate(z2_flags, start = 1) if val != 0})
        locs_to_send.update({board_id + i + 24 for i, val in enumerate(z3_flags, start = 1) if val != 0})
        locs_to_send.update({board_id + i + 43 for i, val in enumerate(z4_flags, start = 1) if val != 0})
        locs_to_send.update({board_id + i + 65 for i, val in enumerate(z5_flags, start = 1) if val != 0})
        locs_to_send.update({board_id + i + 71 for i, val in enumerate(z6_flags, start = 1) if val != 0})
        if locs_to_send != self.local_checked_locations:
            self.local_checked_locations = locs_to_send
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": list(locs_to_send),
            }])


        total_coin_items_received = sum(
            1 for item_id in ctx.items_received if item_id.item == 1
        ) * 3
        await bizhawk.write(ctx.bizhawk_ctx, [
            (FILLER_COINS_ADDR, [total_coin_items_received & 0xFF], "RDRAM"),
        ])
        
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
        SS = any(
            item_id.item == board_id + 8 for item_id in ctx.items_received
        )
        if SS and board_id != 0:
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL,
            }])