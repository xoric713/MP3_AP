from worlds.AutoWorld import World, WebWorld
from dataclasses import dataclass
from Options import PerGameCommonOptions
from BaseClasses import ItemClassification

from .items import MarioParty3Item, get_item_table
from .locations import get_location_table
from .regions import create_regions
from .options import MP3Options

class MP3WebWorld(WebWorld):
    theme = "partyTime"
    tutorials = []

class MarioParty3(World):
    game = "Mario Party 3"
    web = MP3WebWorld()
    options_dataclass = MP3Options
    temp = get_item_table([0,1])
    item_name_to_id = temp
    location_name_to_id = get_location_table([0,1])
    
    item_name_groups = {}
    location_name_groups = {}
    
    def set_rules(self):
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has("AP Test Board - Super Star!", self.player)
    
    def create_regions(self):
        create_regions(self)
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