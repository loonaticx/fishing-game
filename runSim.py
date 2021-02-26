from rich.console import Console
from rich.table import Column, Table
import FishGameGlobals
import FishGameSim

# maybe refactor to runAutoSim instead of runSim

# https://pythonawesome.com/a-python-library-for-rich-text-and-beautiful-formatting-in-the-terminal/
class runSim:
    def __init__(self):
        self.globals = FishGameGlobals
        self.playgroundZones = self.globals.PlaygroundZoneIDs
        rod = self.setRodID()
        loc = self.setLocationID()
        sim = FishGameSim(rod, loc, num, succ)
        #sim.showFishOptions(self.table) TOO EARLY
        pass

    def showOptions(self):
        self.table = Table(show_header=True, header_style="bold magenta")
        #table.add_column("Fishing Rods", style="dim", width=12)
        #table.add_column("Rod IDs")

        self.table.add_column("Locations")
        self.table.add_column("Location IDs")

    def getOptions(self, table):
        playgroundIDs = []
        playgroundNames = []
        for id in self.playgroundZones:
            playgroundIDs.append(id)
            playgroundNames.append(self.playgroundZones[id])

        table.add_row(playgroundNames)
        table.add_row(playgroundIDs)

        pass # This is where we make a list and do a for loop while initializing this class

    def setRodID(self):
        print("Set Rod ID")
        print("1: Bamboo \n 2: Wood .. whatever")
        rodID = input()
        return rodID

    def setLocationID(self):
        print("Which location")
        locationID = input()
        return locationID