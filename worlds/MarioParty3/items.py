from BaseClasses import Item, ItemClassification
from . import boards 

class MarioParty3Item(Item):
    game = "Mario Party 3"
    
def get_item_table(boardlist):
    output = {}
    content = []
    for i in range(2):
        if i in boardlist:
            if i == 0:
                content.append(boards.content.datacontent())
                output.update(content[-1].create_item_table())
            elif i == 1:
                content.append(boards.aptestworld.content.APtestcontent(i))
                output.update(content[-1].create_item_table())
    return output