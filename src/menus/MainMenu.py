"""
this is the first menu that is displayed to the player
"""

from menus.MenuBase import MenuBase
from menus.MenuItems import MainMenuItems
from fishbase.FishGameGlobals import MainMenuOptions


class MainMenu(MenuBase):
    def __init__(self):
        super().__init__()
        self.title = "Main Menu"
        self.items = MainMenuItems
        self.menuOption = MainMenuOptions

    def enterMenu(self, printHeader=False, headerText=""):
        super().enterMenu(printHeader, headerText)
        context.MENU_MODE = self.result


if __name__ == "__main__":
    from fishbase.FishBase import FishBase

    base = FishBase()
    base.mainMenu.enterMenu()
