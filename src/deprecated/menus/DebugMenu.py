from menus.MenuBase import MenuBase
from fishbase.FishGameGlobals import *
from menus.MenuItems import *


class DebugMenu(MenuBase):
    def __init__(self):
        super().__init__()
        self.title = "Fishing Rod Menu"
        self.items = RodMenuItems
        self.menuOption = GameMenuOptions

    def enterMenu(self, printHeader=False, headerText=""):
        super().enterMenu(printHeader, headerText)
        context.GAME_MODE = self.result
