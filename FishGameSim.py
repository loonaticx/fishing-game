class FishGameSim(FishGame):
    """
    Will also control
    ...idk fish genus.. not sure.. i think so
    FishGame.FishGameGlobals i think works
    """
    def __init__(self, rodID, locationID, numberCasts, successRatio):
        FishGame.__init__()
        self.rodID = rodID
        self.locationID = locationID
        self.numberCasts = numberCasts
        self.successRatio = successRatio  # Default 0.8
        pass

    def showFishOptions(self, table):
        table.add_row("Put all the possible fish that can be caught here")

    def configureRod(rodID):
        self.rodID = rodID

    def configureLocation(locationID):
        self.locationID = locationID

    def configureCast(numCasts):
        self.numCasts = numCasts

    def configureSuccess(successRatio):
        self.successRatio = successRatio
