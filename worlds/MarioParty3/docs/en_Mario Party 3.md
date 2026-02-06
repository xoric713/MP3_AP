# Mario Party 3

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Locations and items are defined by the board content under `worlds/MarioParty3/boards/`. The current implementation uses
custom boards created with Party Planner 64, not the vanilla boards. Board checks are turned into Archipelago locations,
and board items are placed into the item pool.

## What is the goal of Mario Party 3 when randomized?

The current goal is to obtain `AP Test Board - Super Star!`.

## What items and locations get shuffled?

The shuffled locations and items come from the selected board content. Progression items include keys and the Super Star.
Useful items include Shrooment. Filler items are coin/item bundles.

## Which items can be in another player's world?

Any shuffled item can appear in another player's world.

## When the player receives an item, what happens?

Items are applied by the BizHawk client and Lua connector and show up in-game at the start of your next turn. If a player has any items gained either in game or via archipelago, then the inventory menu opens at the start of your turn and allows you to select an item to put into slot 0 for the turn. 
current warp blocks and magic lamps are illegal due to progression balancing, so they are re rolled into a legal item. NPCs still can use magic lamps, as the don't affect the player.