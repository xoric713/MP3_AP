from __future__ import annotations

from typing import TYPE_CHECKING, Set
from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .boards.aptestworld import watcher
from .boards import watcher as W


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


INV_ADDR = 0x007E0000  # u8[16] (not used here)



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
        self.watcher = None
        self.global_watcher = W.Watcher()
        self.board = None

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
        ctx.want_slot_data = True
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
            ])
        except bizhawk.RequestFailedError:
            return  # reconnect loop will handle it
        board_id = int.from_bytes(reads[1], "big")
        if board_id == 1000 and board_id != self.board:
            logger.info(f"On board: AP Test Board")
            self.watcher = watcher.APTBwatcher()
            self.board = board_id
        await self.global_watcher.update(ctx)
        if self.watcher:
            await self.watcher.update(ctx)