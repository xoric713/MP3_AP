from worlds.AutoWorld import World, WebWorld
from dataclasses import dataclass
from Options import PerGameCommonOptions
from BaseClasses import ItemClassification, Tutorial

from .items import MarioParty3Item, get_item_table
from .locations import get_location_table
from .regions import create_regions
from .Options import MP3Options

class MP3WebWorld(WebWorld):
    theme = "partyTime"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "How to set up Mario Party 3 with Archipelago.",
        "English",
        "setup.md",
        "setup/en",
        ["xoric713"],
    )]

class MarioParty3(World):
    game = "Mario Party 3"
    web = MP3WebWorld()
    options_dataclass = MP3Options
    temp = get_item_table([0,1])
    item_name_to_id = temp
    location_name_to_id = get_location_table([0,1])
    
    def fill_slot_data(self)->dict:
        return {
            "player_names": self.options.PlayerChar.value,
            "com1_names": self.options.COM1Char.value,
            "com2_names": self.options.COM2Char.value,
            "com3_names": self.options.COM3Char.value,
            "ap_test_board_enabled": self.options.ap_test_board_enabled.value,
            "ap_test_board_turn_count": self.options.ap_test_board_turn_count.value,
            "progturns": self.options.progturns.value,
        }
    
    def set_rules(self):
        if self.options.ap_test_board_enabled.value and self.options.progturns.value:
            ap_turns = self.options.ap_test_board_turn_count.value * self.options.ap_test_board_enabled.value
            final_turn = f"AP Test Board - 1st place on Turn: {ap_turns:02}"
            self.multiworld.completion_condition[self.player] = \
                lambda state, loc=final_turn: state.can_reach_location(loc, self.player)
        elif self.options.ap_test_board_enabled.value:
            self.multiworld.completion_condition[self.player] = \
                lambda state: state.has("AP Test Board - Zone 6 Key", self.player)
    def create_regions(self):
        ap_turns = self.options.ap_test_board_turn_count.value * self.options.ap_test_board_enabled.value 
        create_regions(self, ap_turns, self.options.progturns.value)
        self.multiworld.get_region("Menu", self.player)
        self.origin_region_name = "Menu"
        
    def create_item(self, name: str, cls):
        return MarioParty3Item(name, cls, self.item_name_to_id[name], self.player)
    
    def create_items(self):
        from pprint import pprint
        pprint(self.item_name_to_id)
        pprint(self.location_name_to_id)
        filler_list = []
        count = len(self.location_name_to_id)
        if len(self.item_name_to_id) > count:
            raise Exception("More items than locations, cannot create world!")
        for item_name in self.item_name_to_id.keys():
            iname = item_name.lower()
            if ("key" in iname and "skeleton" not in iname) or "super star" in iname:
                item = self.create_item(item_name, ItemClassification.progression)
                self.multiworld.itempool.append(item)
                count -= 1
            elif "progressive turn" in iname and self.options.progturns.value:
                for i in range(self.options.ap_test_board_turn_count.value-1):
                    item = self.create_item(item_name, ItemClassification.progression)
                    count -= 1
                    self.multiworld.itempool.append(item)
            elif "wacky watch" in iname:
                k = 0
                for i in range(self.options.ap_test_board_turn_count.value):
                    if k >= 5:
                        item = self.create_item(item_name, ItemClassification.progression)
                        count -= 1
                        self.multiworld.itempool.append(item)
                        k = 0
                    else:
                        k += 1
            elif "shrooment" in iname:
                item = self.create_item(item_name, ItemClassification.useful)
                self.multiworld.itempool.append(item)
                count -= 1
                item = self.create_item(item_name, ItemClassification.useful)
                self.multiworld.itempool.append(item)
                count -= 1
            elif "coin" in iname or "item" in iname:
                if "coins" in iname:
                    filler_list.append((item_name, ItemClassification.filler))
                    filler_list.append((item_name, ItemClassification.filler))
                    filler_list.append((item_name, ItemClassification.filler))
                    filler_list.append((item_name, ItemClassification.filler))
                filler_list.append((item_name, ItemClassification.filler))
        if count > 0 and not filler_list:
            raise Exception("Not enough filler items to fill the world!")
        while count > 0:
            item_name, cls = self.multiworld.random.choice(filler_list)
            item = self.create_item(item_name, cls)
            self.multiworld.itempool.append(item)
            count -= 1