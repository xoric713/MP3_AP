from BaseClasses import Region, Entrance
from .locations import MarioParty3Location, get_location_table
from worlds.generic.Rules import set_rule

from . import boards

def link_regions(player, source: Region, target: Region, name: str):
    entrance = Entrance(player, name, source)
    source.exits.append(entrance)
    entrance.connect(target)
    return entrance

def create_regions(world, turns, progturns):
    mw = world.multiworld
    p = world.player
    
    boards.regions.create_regions(mw, p)
    boards.aptestworld.regions.create_regions(mw, p, turns, progturns)
    open_board = link_regions(p, mw.get_region("Menu", p), mw.get_region("APTB_0", p), "Open Board Select Menu")
    set_rule(open_board, lambda state: True)