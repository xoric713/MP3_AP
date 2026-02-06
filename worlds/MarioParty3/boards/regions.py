from BaseClasses import Region, Entrance
from ..locations import MarioParty3Location, get_location_table
from worlds.generic.Rules import set_rule

def link_regions(player, source: Region, target: Region, name: str):
    entrance = Entrance(player, name, source)
    source.exits.append(entrance)
    entrance.connect(target)
    return entrance

def create_regions(mw,p):
    
    menu = Region("Menu", p, mw)
    
    mw.regions += [menu]