from BaseClasses import Region, Entrance
from ...locations import MarioParty3Location, get_location_table
from worlds.generic.Rules import set_rule

def link_regions(player, source: Region, target: Region, name: str):
    entrance = Entrance(player, name, source)
    source.exits.append(entrance)
    entrance.connect(target)
    return entrance

def create_regions(mw,p,turns,prog):
    
    APTB_0 = Region("APTB_0", p, mw)
    APTB_1 = Region("APTB_1", p, mw)
    APTB_2 = Region("APTB_2", p, mw)
    APTB_3 = Region("APTB_3", p, mw)
    APTB_4 = Region("APTB_4", p, mw)
    APTB_5 = Region("APTB_5", p, mw)
    APTB_6 = Region("APTB_6", p, mw)
    turnslist = []
    
    door2 = link_regions(p, APTB_0, APTB_1, "AP Test Board Zone 0 -> Zone 1")
    set_rule(door2, lambda state: state.has("AP Test Board - Zone 1 Key", p))
    door3 = link_regions(p, APTB_1, APTB_2, "AP Test Board Zone 1 -> Zone 2")
    set_rule(door3, lambda state: state.has("AP Test Board - Zone 2 Key", p))
    door4 = link_regions(p, APTB_2, APTB_3, "AP Test Board Zone 2 -> Zone 3")
    set_rule(door4, lambda state: state.has("AP Test Board - Zone 3 Key", p))
    door5 = link_regions(p, APTB_3, APTB_4, "AP Test Board Zone 3 -> Zone 4")
    set_rule(door5, lambda state: state.has("AP Test Board - Zone 4 Key", p))
    door6 = link_regions(p, APTB_3, APTB_5, "AP Test Board Zone 3 -> Zone 5")
    set_rule(door6, lambda state: state.has("AP Test Board - Zone 5 Key", p))
    door7 = link_regions(p, APTB_4, APTB_6, "AP Test Board Zone 4 -> Zone 6")
    set_rule(door7, lambda state: state.has("AP Test Board - Zone 6 Key", p))
    door8 = link_regions(p, APTB_5, APTB_6, "AP Test Board Zone 5 -> Zone 6")
    set_rule(door8, lambda state: state.has("AP Test Board - Zone 6 Key", p))
    door9 = link_regions(p, APTB_6, APTB_5, "AP Test Board Zone 6 -> Zone 5")
    set_rule(door9, lambda state: state.has("AP Test Board - Zone 5 Key", p))
    
    table = get_location_table([1])
    for loc_name, loc_id in table.items():
        if loc_name.startswith("AP Test Board - Zone 0"):
            location = MarioParty3Location(p, loc_name, loc_id, APTB_0)
            APTB_0.locations.append(location)
        elif loc_name.startswith("AP Test Board - Zone 1"):
            location = MarioParty3Location(p, loc_name, loc_id, APTB_1)
            APTB_1.locations.append(location)
        elif loc_name.startswith("AP Test Board - Zone 2"):
            location = MarioParty3Location(p, loc_name, loc_id, APTB_2)
            APTB_2.locations.append(location)
        elif loc_name.startswith("AP Test Board - Zone 3"):
            location = MarioParty3Location(p, loc_name, loc_id, APTB_3)
            APTB_3.locations.append(location)
        elif loc_name.startswith("AP Test Board - Zone 4"):
            location = MarioParty3Location(p, loc_name, loc_id, APTB_4)
            APTB_4.locations.append(location)
        elif loc_name.startswith("AP Test Board - Zone 5"):
            location = MarioParty3Location(p, loc_name, loc_id, APTB_5)
            APTB_5.locations.append(location)
        elif loc_name.startswith("AP Test Board - Zone 6"):
            location = MarioParty3Location(p, loc_name, loc_id, APTB_6)
            APTB_6.locations.append(location)
        elif loc_name.startswith("AP Test Board - 1st place on Turn"):
            TC = int(loc_name.split("Turn: ")[1])
            if TC <= turns:
                turnslist.append((loc_name, loc_id))
    turnslist.sort(key=lambda x: int(x[0].split("Turn: ")[1]))
    for loc_name, loc_id in turnslist:
        location = MarioParty3Location(p, loc_name, loc_id, APTB_0)
        APTB_0.locations.append(location)
        if prog:
            turn_num = int(loc_name.split("Turn: ")[1])
            req = turn_num - 1  # Turn 01 is free
            set_rule(location, lambda state, req=req: state.count("AP Test Board - Progressive Turns", p) >= req)
                
    
    mw.regions += [APTB_0, APTB_1, APTB_2, APTB_3, APTB_4, APTB_5, APTB_6]