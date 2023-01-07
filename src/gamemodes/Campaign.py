from fishbase.EnumBase import *


class Campaign:
    def __init__(self):
        self.wantTutorial = 1
        context.ROD_ID = FishingRod.TWIG_ROD
        context.LOCATION_ID = Location.ToontownCentral
        context.BUCKET_SIZE_MAX = 20

    def enterCampaign(self):
        # You are a 15 laff toon in ttc
        # You start with a twig rod, default bank amount
        # Thankfully you do not need to go on the Trolley for Jellybeans, Flippy spared you some
        # However, he recommends fishing in the playground before venturing to other ponds.
        # Fisherman Freddy asks if you need some instructions before fishing for the first time
        pass

    def enterTutorial(self):
        pass
