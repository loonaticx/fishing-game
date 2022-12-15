from menus.MenuBase import MenuBase
from menus.MenuItems import MenuGameModeItems
from fishbase.FishGameGlobals import GameMenuOptions


class LocationMenu(MenuBase):

    def __init__(self):
        super().__init__()
        self.title = "Select Game Mode"
        self.items = MenuGameModeItems
        self.prompt = "Which game mode would you like to play?"
        self.menuOption = GameMenuOptions


if __name__ == "__main__":
    from fishbase.FishBase import FishBase

    FishBase()
    menu = LocationMenu()
    menu.enterMenu()
