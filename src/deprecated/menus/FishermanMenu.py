"""
Menu that is generated when talking to a fisherman

Initial menu is basic;
> Sell Fish
> Buy Rods
> Tutorial
> Go back
"""

"""
Buy rods --> upgrade
Upgrades may include features such as
- upgrade rod
- unlocking stats that show percent chance and stuff
"""

from menus.MenuBase import MenuBase
from menus.MenuItems import FishermanMenuItems
from fishbase.FishGameGlobals import GameMenuOptions


class FishermanMenu(MenuBase):
    def __init__(self):
        super().__init__()
        self.title = "Fisherman Menu"
        self.items = FishermanMenuItems
        self.menuOption = GameMenuOptions
