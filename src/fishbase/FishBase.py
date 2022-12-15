from rich.console import Console
from PyInquirer import prompt
from rich.markdown import Markdown
from fishbase.FishContext import FishContext
from menus.GameSelectionMenu import GameSelectionMenu
from menus.MainMenu import MainMenu
from menus.DebugMenu import DebugMenu
from menus.RodMenu import RodMenu


class FishBase:
    console = Console()
    context = FishContext()

    def __init__(self):
        __builtins__['console'] = self.console
        __builtins__['context'] = self.context
        __builtins__['prompt'] = prompt
        console.print("Pre-generating menus...")
        self.generateMenus()
        self.refreshTitleScreen()

    def generateMenus(self):
        self.mainMenu = MainMenu()
        self.gameModeMenu = GameSelectionMenu()
        self.fishingRodMenu = RodMenu()
        self.debugMenu = DebugMenu()

    def refreshTitleScreen(self):
        console.clear()
        console.print("Welcome to [red]Loonatic's[/red] [bold blue]Fishing Game Simulator![/bold blue] v.0.1")
        console.print(Markdown("---"))
