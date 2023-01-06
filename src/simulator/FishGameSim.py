from fishbase.FishGameGlobals import fishDict
from fishbase.FishLocalizer import FishSpeciesNames
from simulator.SimulatorBase import FishGame
from fishbase.EnumBase import *


class FishGameSim(FishGame):
    """
    Will also control
    ...idk fish genus.. not sure.. i think so
    FishGame.FishGameGlobals i think works
    """

    def __init__(self, rodID, locationID, numberCasts=1, successRatio=0.8):
        FishGame.__init__(self)
        self.rodID = rodID
        self.locationID = locationID
        self.numberCasts = numberCasts
        self.successRatio = successRatio  # Default 0.8
        pass

    def showFishOptions(self, table):
        table.add_row("Put all the possible fish that can be caught here")

    def configureRod(self, rodID):
        self.rodID = rodID

    def configureLocation(self, locationID):
        self.locationID = locationID

    def configureCast(self, numCasts):
        self.numCasts = numCasts

    def configureSuccess(self, successRatio):
        self.successRatio = successRatio

    def canCastRod(self):
        if context.JELLYBEANS_CURRENT - 1 < 0:
            return False
        return True


if __name__ == "__main__":
    rod = FishingRod.TWIG_ROD
    location = Location.TOONTOWN_CENTRAL
    numberCasts = 69
    successRatio = 1
    game = FishGameSim(rod, location, numberCasts, successRatio)
    game.calculateFishLocations(fishDict)
    # game.generateFishingReport()
    pondInfo = game.getSimplePondInfo()
    # print(pondInfo.get(Location.TOONTOWN_CENTRAL))
    for entry in pondInfo.get(Location.TOONTOWN_CENTRAL):
        genus, species = entry
        print(FishSpeciesNames.get(genus)[species])
