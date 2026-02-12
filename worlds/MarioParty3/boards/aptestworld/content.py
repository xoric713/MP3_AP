from ..content import datacontent

class APtestcontent(datacontent):
    def __init__(self, idx):
        super().__init__()
        self.Version = "0.0.1"
        self.Code = "APTB"
        self.Name = "AP Test Board"
        self.index = idx * 1000
        self.locations = {
            "Z01": "Zone 0 - Space 01",
            "Z02": "Zone 0 - Space 02",
            "Z03": "Zone 0 - Space 03",
            "Z04": "Zone 0 - Space 04",
            "Z05": "Zone 0 - Space 05",
            "Z06": "Zone 0 - Space 06",
            "Z07": "Zone 0 - Space 07",
            "Z0?": "Zone 0 - Happening Space",
            "Z11": "Zone 1 - Space 01",
            "Z12": "Zone 1 - Space 02",
            "Z13": "Zone 1 - Space 03",
            "Z14": "Zone 1 - Space 04",
            "Z15": "Zone 1 - Space 05",
            "Z16": "Zone 1 - Space 06",
            "Z17": "Zone 1 - Space 07",
            "Z1?": "Zone 1 - Happening Space",
            "Z21": "Zone 2 - Space 01",
            "Z22": "Zone 2 - Space 02",
            "Z23": "Zone 2 - Space 03",
            "Z24": "Zone 2 - Space 04",
            "Z25": "Zone 2 - Space 05",
            "Z26": "Zone 2 - Space 06",
            "Z27": "Zone 2 - Space 07",
            "Z2?": "Zone 2 - Happening Space",
            "Z31": "Zone 3 - Space 01",
            "Z32": "Zone 3 - Space 02",
            "Z33": "Zone 3 - Space 03",
            "Z34": "Zone 3 - Space 04",
            "Z35": "Zone 3 - Space 05",
            "Z36": "Zone 3 - Space 06",
            "Z37": "Zone 3 - Space 07",
            "Z38": "Zone 3 - Space 08",
            "Z39": "Zone 3 - Space 09",
            "Z310": "Zone 3 - Space 10",
            "Z311": "Zone 3 - Space 11",
            "Z312": "Zone 3 - Space 12",
            "Z313": "Zone 3 - Space 13",
            "Z314": "Zone 3 - Space 14",
            "Z315": "Zone 3 - Space 15",
            "Z316": "Zone 3 - Space 16",
            "Z317": "Zone 3 - Space 17",
            "Z318": "Zone 3 - Space 18",
            "Z3?": "Zone 3 - Happening Space",
            "Z41": "Zone 4 - Space 01",
            "Z42": "Zone 4 - Space 02",
            "Z43": "Zone 4 - Space 03",
            "Z44": "Zone 4 - Space 04",
            "Z45": "Zone 4 - Space 05",
            "Z46": "Zone 4 - Space 06",
            "Z47": "Zone 4 - Space 07",
            "Z48": "Zone 4 - Space 08",
            "Z49": "Zone 4 - Space 09",
            "Z410": "Zone 4 - Space 10",
            "Z411": "Zone 4 - Space 11",
            "Z412": "Zone 4 - Space 12",
            "Z413": "Zone 4 - Space 13",
            "Z414": "Zone 4 - Space 14",
            "Z415": "Zone 4 - Space 15",
            "Z416": "Zone 4 - Space 16",
            "Z417": "Zone 4 - Space 17",
            "Z418": "Zone 4 - Space 18",
            "Z419": "Zone 4 - Space 19",
            "Z420": "Zone 4 - Space 20",
            "Z4?": "Zone 4 - Happening Space",
            "Z51": "Zone 5 - Space 01",
            "Z52": "Zone 5 - Space 02",
            "Z53": "Zone 5 - Space 03",
            "Z54": "Zone 5 - Space 04",
            "Z55": "Zone 5 - Space 05",
            "Z56": "Zone 5 - Space 06",
            "Z5?": "Zone 5 - Happening Space",
            "Z61": "Zone 6 - Space 01",
            "Z62": "Zone 6 - Space 02",
            "Z63": "Zone 6 - Space 03",
            "Z64": "Zone 6 - Space 04",
            "Z65": "Zone 6 - Space 05",
            "Z66": "Zone 6 - Space 06",
            "Z67": "Zone 6 - Space 07",
            "Z68": "Zone 6 - Space 08",
            "Z69": "Zone 6 - Space 09",
            "Z610": "Zone 6 - Space 10",
            "Z611": "Zone 6 - Space 11",
            "Z612": "Zone 6 - Space 12",
            "Z613": "Zone 6 - Space 13",
            "Z6?": "Zone 6 - Happening Space",
        }
        for i in range(1,51):
            self.locations[f"T{i}"] = f"1st place on Turn: {i:02}"
        self.items = {
            "Z1key": "Zone 1 Key",
            "Z2key": "Zone 2 Key",
            "Z3key": "Zone 3 Key",
            "Z4key": "Zone 4 Key",
            "Z5key": "Zone 5 Key",
            "Z6key": "Zone 6 Key",
            "PShrom": "Progressive Shrooment",
            "APTBPT": "Progressive Turns",
            "I18": "Proggressive Wacky Watch",
        }
    def create_location_table(self) -> dict:
        output = {}
        pointer = self.index + 1
        pointer_index = self.index + 1
        for loc in self.locations.values():
            output[f"AP Test Board - {loc}"] = pointer
            pointer += 1
            if pointer >= 999 + pointer_index:
                raise Exception("Too many locations defined!")
        return output
    def create_item_table(self) -> dict:
        output = {}
        pointer = self.index + 1
        pointer_index = self.index + 1
        for item in self.items.values():
            output[f"AP Test Board - {item}"] = pointer
            pointer += 1
            if pointer >= 999 + pointer_index:
                raise Exception("Too many locations defined!")
        return output
    