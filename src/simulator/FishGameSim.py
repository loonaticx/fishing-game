from FishGame import FishGame


class FishGameSim(FishGame):
    """
    Will also control
    ...idk fish genus.. not sure.. i think so
    FishGame.FishGameGlobals i think works
    """

    def __init__(self, rodID, locationID, numberCasts, successRatio):
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
