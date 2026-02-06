class datacontent():
    def __init__(self):
        self.Version  = "0.0.1"
        self.Code = "Glob"
        self.index = 0
        self.locations = {}
        self.items = {
            "C3": "Coins +3",
            "I0": "Mushroom Item",
            "I1": "Skeleton Key Item",
            "I2": "Poison Mushroom Item",
            "I3": "Reverse Mushroom Item",
            "I4": "Cellular Shopper Item",
            "I5": "--ILLEGAL--WB",  # Warp Block
            "I6": "Plunder Chest Item",
            "I7": "Bowser Phone Item",
            "I8": "Dueling Glove Item",
            "I9": "Lucky Lamp Item",
            "I10": "Golden Mushroom Item",
            "I11": "Boo Bell Item",
            "I12": "Boo Repellant Item",
            "I13": "Bowser Suit Item",
            "I14": "--ILLEGAL--ML",  # Magic Lamp
            "I15": "Koopa Card Item",
            "I16": "Barter Box Item",
            "I17": "Lucky Coin Item",
            "I18": "Wacky Watch Item",
    }


    def create_location_table(self) -> dict:
        output = {}
        pointer = 1
        pointer_index = 1
        for loc in self.locations.values():
            output[loc] = pointer
            pointer += 1
            if pointer >= 999 + pointer_index:
                raise Exception("Too many locations defined!")
        return output
            
    def create_item_table(self) -> dict:
        output = {}
        pointer = 1
        pointer_index = pointer
        for item in self.items.values():
            output[item] = pointer
            pointer += 1
            if pointer >= 999 + pointer_index:
                raise Exception("Too many items defined!")
        return output

if __name__ == "__main__":
    import pprint
    data = datacontent()
    pprint.pprint(data.create_location_table())
    pprint.pprint(data.create_item_table())