from importlib import import_module

BOARD_OPTION_MODULES = [
    'worlds.MarioParty3.boards.aptestworld.options',
]
def iter_board_option_mixins():
    for mod_path in BOARD_OPTION_MODULES:
        mod = import_module(mod_path)
        mixin = getattr(mod, 'BoardOptionsMixin', object)
        if mixin is not object:
            yield mixin