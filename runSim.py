"""
ToontownFishingSimulator Main Menu

Contains user interface for setting up the fishing simulator parameters
"""

from rich.table import Column, Table
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.prompt import Prompt

import FishGameGlobals


# https://pythonawesome.com/a-python-library-for-rich-text-and-beautiful-formatting-in-the-terminal/
from FishGameSim import FishGameSim


class RunSimulator:
    console = Console()

    def __init__(self):
        self.console.print("Welcome to [red]Loonatic's[/red] [bold blue]Fishing Game Simulator![/bold blue] v.0.1")
        self.globals = FishGameGlobals
        self.locationData = self.globals.LocationData
        menuMode = self.showMenu()
        self.console.clear()
        gameMode = self.enterGameSelection(menuMode)
        self.console.clear()

        # relocate
        rod = self.setRodID()
        self.console.clear()
        loc = self.setLocationID()
        num = 30
        succ = 30
        sim = FishGameSim(rod, loc, num, succ)
        # sim.showFishOptions(self.table)  # TOO EARLY
        pass

    def showMenu(self):
        # would you like to check data or play the game?
        # would you like to do free play or fisherman mode?
        menuTable = Table(show_header = False, header_style = "bold magenta")
        menuTable.add_column("Select Mode", style = "dim")
        menuTable.add_column("Mode ID", style = "dim")

        menuTable.add_row(
            "Check Fishing Statistics", "1",
        )
        menuTable.add_row(
            "Play Fishing Game", "2"
        )
        print(menuTable)

        return Prompt.ask("Which option would you like to choose?")

    def enterGameSelection(self, menuChoice):
        if menuChoice == "1":
            menuChoice = "2"

        if menuChoice == "2":
            gameModeTable = Table(show_header = True, header_style = "bold magenta")
            gameModeTable.add_column("Select Game Mode", style = "dim")

            gameModeTable.add_row(
                "Free Play", "1", "Description about Free Play"
            )
            gameModeTable.add_row(
                "Campaign", "2", "Description about Campaign"
            )
            # give x amount of trials and generate results
            gameModeTable.add_row(
                "AutoSim", "3", "Description about AutoSim"
            )
            self.console.print(gameModeTable)
            return Prompt.ask("Which game mode would you like to play?")

    def buildLocations(self, table, context=None):
        # context = FishingContext = enum class? holds context if player is in freeplay/campaign
        # and if they are in campaign it holds data such as current location, locked locations
        # to change the colors accordingly
        for id in self.locationData:
            pgName = self.locationData[id][0]
            pgColor = self.locationData[id][1]
            table.add_row(str(id), f"[{pgColor}]{pgName}[/{pgColor}]")

        # table.add_row(playgroundNames)
        # table.add_row(playgroundIDs)

        pass  # This is where we make a list and do a for loop while initializing this class

    def setRodID(self):
        rodTable = Table(show_header = True, header_style = "bold magenta")
        rodTable.add_column("Rod ID")
        rodTable.add_column("Rod Name")
        rodTable.add_column("Rod Cost")

        rodTable.add_row(
            "1", "Bamboo Rod", "69"
        )
        rodTable.add_row(
            "2", "Twig Rod", "22"
        )
        self.console.print(rodTable)

        rodID = Prompt.ask("Choose your fishing rod")
        if type(rodID) == str:
            rodID = rodID.lower()
            if " rod" in rodID:
                rodID = rodID[:-4]
        return rodID

    def setLocationID(self):
        locationTable = Table(show_header = True, header_style = "bold magenta")
        locationTable.add_column("Location ID")
        locationTable.add_column("Location Name")
        self.buildLocations(locationTable)
        self.console.print(locationTable)

        locationID = Prompt.ask("Where would you like to fish?")
        return locationID


RunSimulator()
