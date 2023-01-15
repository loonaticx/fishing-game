"""
Fishing Rod Menu
"""

from menus.MenuBase import MenuBase
from menus.MenuItems import RodMenuItems
from fishbase.FishGameGlobals import GameMenuOptions


class RodMenu(MenuBase):
    def __init__(self):
        super().__init__()
        self.title = "Fishing Rod Menu"
        self.items = RodMenuItems
        self.menuOption = GameMenuOptions


if __name__ == "__main__":
    from fishbase.FishBase import FishBase

    FishBase()
    menu = RodMenu()
    menu.enterMenu()
