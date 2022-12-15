from fishbase import FishLocalizer
# Should not get any pond info, though listing below zones should be ok

# Zones
ToontownCentral = 10
PunchlinePlace = 11
LoopyLane = 12
SillyStreet = 13

DonaldsDock = 20
BarnacleBoulevard = 21
SeaweedStreet = 22
LighthouseLane = 23

DaisyGardens = 30
ElmStreet = 31
MapleStreet = 32
OakStreet = 33

MinniesMelodyland = 40
AltoAvenue = 41
BaritoneBoulevard = 42
TenorTerrace = 43

TheBrrrgh = 50
WalrusWay = 51
SleetStreet = 52
PolarPlace = 53

DonaldsDreamland = 60
LullabyLane = 61
PajamaPlace = 62

OutdoorZone = 70

# These are hood ids, but they are not zone ids.
Tutorial =             15000
MyEstate =             16000

# Minigolf hood ids
GolfZone =             17000

# Party zone hood id
PartyHood =            18000

DefaultBucketSize = 20

from fishbase.EnumBase import *

MainMenuOptions = {
    "none": MainMenuChoice.NONE,
    "play": MainMenuChoice.FISHING_GAME,
    "review": MainMenuChoice.FISHING_STATS,
    "simulate": MainMenuChoice.FISHING_AUTOSIM
}

GameMenuOptions = {
    "back": GameMode.NONE,  # "go back"
    "free": GameMode.FREE_PLAY,
    "campaign": GameMode.CAMPAIGN,
}


FishermanMenuOptions = {
    "back": GameMode.NONE,  # "go back"
    "sell": GameMode.FREE_PLAY,
    "buy": GameMode.FREE_PLAY,
    "tutorial": GameMode.CAMPAIGN,
}




#### PLAYGROUND DATA
LocationData = {
    1: ['Toontown Central Playground', 'gold3', ToontownCentral],
    2: ['Punchline Place', 'gold3', PunchlinePlace],
    3: ['Loopy Lane', 'gold3', LoopyLane],
    4: ['Silly Street', 'gold3', SillyStreet]
}

Nothing = 0
QuestItem = 1
FishItem = 2
JellybeanItem = 3
BootItem = 4
GagItem = 5
OverTankLimit = 8
FishItemNewEntry = 9
FishItemNewRecord = 10
ProbabilityDict = {93: FishItem,
                   94: JellybeanItem,
                   100: BootItem}
SortedProbabilityCutoffs = list(ProbabilityDict.keys())
SortedProbabilityCutoffs.sort()

MAX_RARITY = 10
MAX_RARITY_NERFS = 7
GlobalRarityDialBase = 4.3
FishingAngleMax = 50.0
OVERALL_VALUE_SCALE = 15
RARITY_VALUE_SCALE = 0.2
WEIGHT_VALUE_SCALE = 0.05 / 16.0
COLLECT_NO_UPDATE = 0
COLLECT_NEW_ENTRY = 1
COLLECT_NEW_RECORD = 2


FISH_PER_BONUS = 10
TrophyDict = {0: (FishLocalizer.FishTrophyNameDict[0],),
              1: (FishLocalizer.FishTrophyNameDict[1],),
              2: (FishLocalizer.FishTrophyNameDict[2],),
              3: (FishLocalizer.FishTrophyNameDict[3],),
              4: (FishLocalizer.FishTrophyNameDict[4],),
              5: (FishLocalizer.FishTrophyNameDict[5],),
              6: (FishLocalizer.FishTrophyNameDict[6],)}
WEIGHT_MIN_INDEX = 0
WEIGHT_MAX_INDEX = 1
RARITY_INDEX = 2
ZONE_LIST_INDEX = 3
Anywhere = 1


"""
0 - Balloon
2 - Cat
4 - Clown
6 - Frozen
8 - Star
10 - Holey
12
14
16
18
20
22
24
26
28
30
32
34
"""

# Genus is stored as an even number just to perforate the space for future additions
# FishDict stores a dictionary of fish properties
# GENUS : SPECIES_LIST
# SPECIES_LIST is a list of SPECIES
# Each SPECIES defines properties: (WEIGHT_MIN, WEIGHT_MAX, RARITY, ZONE_LIST)
__fishDict = {
    0: ( ( 1, 3, 1, (Anywhere, ) ), # Balloon Fish
         ( 1, 1, 4, (ToontownCentral, Anywhere) ), # Hot Air Balloon Fish
         ( 3, 5, 5, (PunchlinePlace, TheBrrrgh) ), # Weather Balloon Fish
         ( 3, 5, 3, (SillyStreet, DaisyGardens) ), # Water Balloon Fish
         ( 1, 5, 2, (LoopyLane, ToontownCentral) ), # Red Balloon Fish
         ),
    2: ( ( 2, 6, 1, (DaisyGardens, Anywhere) ), # Cat Fish
         ( 2, 6, 9, (ElmStreet, DaisyGardens) ), # Siamese Cat Fish
         ( 5, 11, 4, (LullabyLane, ) ), # Alley Cat Fish
         ( 2, 6, 3, (DaisyGardens, MyEstate) ), # Tabby Cat Fish
         ( 5, 11, 2, (DonaldsDreamland, MyEstate) ), # Tom Cat Fish
         ),
    4: ( ( 2, 8, 1, (ToontownCentral, Anywhere) ), # Clown Fish
         ( 2, 8, 4, (ToontownCentral, Anywhere) ), # Sad Clown Fish
         ( 2, 8, 2, (ToontownCentral, Anywhere) ), # Party Clown Fish
         ( 2, 8, 6, (ToontownCentral, MinniesMelodyland) ), # Circus Clown Fish
         ),
    6: ( ( 8, 12, 1, (TheBrrrgh, ) ), # Frozen Fish
         ),
    8: ( ( 1, 5, 1, (Anywhere, ) ), # Star Fish
         ( 2, 6, 2, (MinniesMelodyland, Anywhere) ), # Five Star Fish
         ( 5, 10, 5, (MinniesMelodyland, Anywhere) ), # Rock Star Fish
         ( 1, 5, 7, (MyEstate, Anywhere) ), # Shining Star Fish
         ( 1, 5, 10, (MyEstate, Anywhere) ), # All Star Fish
         ),
    10: ( ( 6, 10, 9, (MyEstate, Anywhere) ), # Holey Mackerel
          ),
    12: ( ( 7, 15, 1, (DonaldsDock, Anywhere) ), # Dog Fish
          ( 18, 20, 6, (DonaldsDock, MyEstate) ), # Bull Dog Fish
          ( 1, 5, 5, (DonaldsDock, MyEstate) ), # Hot Dog Fish
          ( 3, 7, 4, (DonaldsDock, MyEstate) ), # Dalmation Dog Fish
          ( 1, 2, 2, (DonaldsDock, Anywhere) ), # Puppy Dog Fish
          ),
    14: ( ( 2, 6, 1, (DaisyGardens, MyEstate, Anywhere) ), # Amore Eel
          ( 2, 6, 3, (DaisyGardens, MyEstate) ), # Electric Amore Eel
          ),
    16: ( ( 4, 12, 5, (MinniesMelodyland, Anywhere) ), # Nurse Shark
          ( 4, 12, 7, (BaritoneBoulevard, MinniesMelodyland) ), # Clara Nurse Shark
          ( 4, 12, 8, (TenorTerrace, MinniesMelodyland) ), # Florence Nurse Shark
          ),

    # NOTE: Do not change the locations of the King Crab. They have been discussed in
    # marketing materials as being in these spots.
    18: ( ( 2, 4, 3, (DonaldsDock, Anywhere) ), # King Crab
          ( 5, 8, 7, (TheBrrrgh, ) ), # Alaskan King Crab
          ( 4, 6, 8, (LighthouseLane, ) ), # Old King Crab
          ),

    20: ( ( 4, 6, 1, (DonaldsDreamland, ) ), # Moon Fish
          ( 14, 18, 10, (DonaldsDreamland, ) ), # Full Moon Fish
          ( 6, 10, 8, (LullabyLane, ) ), # Half Moon Fish
          ( 1, 1, 3, (DonaldsDreamland, ) ), # New Moon Fish
          ( 2, 6, 6, (LullabyLane, ) ), # Crescent Moon Fish
          ( 10, 14, 4, (DonaldsDreamland, DaisyGardens) ), # Harvest Moon Fish
          ),
    22: ( ( 12, 16, 2, (MyEstate, DaisyGardens, Anywhere) ), # Sea Horse
          ( 14, 18, 3, (MyEstate, DaisyGardens, Anywhere) ), # Rocking Sea Horse
          ( 14, 20, 5, (MyEstate, DaisyGardens) ), # Clydesdale Sea Horse
          ( 14, 20, 7, (MyEstate, DaisyGardens) ), # Arabian Sea Horse
          ),
    24: ( ( 9, 11, 3, (Anywhere, ) ), # Pool Shark
          ( 8, 12, 5, (DaisyGardens, DonaldsDock) ), # Kiddie Pool Shark
          ( 8, 12, 6, (DaisyGardens, DonaldsDock) ), # Swimming Pool Shark
          ( 8, 16, 7, (DaisyGardens, DonaldsDock) ), # Olympic Pool Shark
          ),
    26: ( ( 10, 18, 2, (TheBrrrgh, ) ), # Brown Bear Acuda
          ( 10, 18, 3, (TheBrrrgh, ) ), # Black Bear Acuda
          ( 10, 18, 4, (TheBrrrgh, ) ), # Koala Bear Acuda
          ( 10, 18, 5, (TheBrrrgh, ) ), # Honey Bear Acuda
          ( 12, 20, 6, (TheBrrrgh, ) ), # Polar Bear Acuda
          ( 14, 20, 7, (TheBrrrgh, ) ), # Panda Bear Acuda
          ( 14, 20, 8, (SleetStreet, TheBrrrgh) ), # Kodiac Bear Acuda
          ( 16, 20, 10, (WalrusWay, TheBrrrgh) ), # Grizzly Bear Acuda
          ),
    28: ( ( 2, 10, 2, (DonaldsDock, Anywhere) ), # Cutthroat Trout
          ( 4, 10, 6, (BarnacleBoulevard, DonaldsDock) ), # Captain Cutthroat Trout
          ( 4, 10, 7, (SeaweedStreet, DonaldsDock) ), # Scurvy Cutthroat Trout
          ),
    30: ( ( 13, 17, 5, (MinniesMelodyland, Anywhere) ), # Piano Tuna
          ( 16, 20, 10, (AltoAvenue, MinniesMelodyland) ), # Grand Piano Tuna
          ( 12, 18, 9, (TenorTerrace, MinniesMelodyland) ), # Baby Grand Piano Tuna
          ( 12, 18, 6, (MinniesMelodyland, ) ), # Upright Piano Tuna
          ( 12, 18, 7, (MinniesMelodyland, ) ), # Player Piano Tuna
          ),
    32: ( ( 1, 5, 2, (ToontownCentral, MyEstate, Anywhere) ), # PB&J Fish
          ( 1, 5, 3, (TheBrrrgh, MyEstate, Anywhere) ), # Grape PB&J Fish
          ( 1, 5, 4, (DaisyGardens, MyEstate) ), # Crunchy PB&J Fish
          ( 1, 5, 5, (DonaldsDreamland, MyEstate) ), # Strawberry PB&J Fish
          ( 1, 5, 10, (TheBrrrgh, DonaldsDreamland) ), # Concord Grape PB&J Fish
          ),
    34: ( ( 1, 20, 10, (DonaldsDreamland, Anywhere) ), # Devil Ray
          ),
    }

# Indexes into the FishDict data
ROD_WEIGHT_MIN_INDEX = 0
ROD_WEIGHT_MAX_INDEX = 1
ROD_CAST_COST_INDEX = 2

# Rods with their associated weight ranges
# Rods can catch the minimum up to the maximum
__rodDict = {
    FishingRod.TWIG_ROD: (0, 4, 1),
    FishingRod.BAMBOO_ROD: (0, 8, 2),
    FishingRod.HARDWOOD_ROD: (0, 12, 3),
    FishingRod.STEEL_ROD: (0, 16, 4),
    FishingRod.GOLD_ROD: (0, 20, 5)
}
rodDict = __rodDict
def getSpecies(genus):
    return __fishDict[genus]

def getGenera():
    return list(__fishDict.keys())

def getNumRods():
    return len(__rodDict)

def getCastCost(rodId):
    return __rodDict[rodId][ROD_CAST_COST_INDEX]

def getTotalNumFish():
    return __totalNumFish # prob wanna remove this and make it a public variable instead

def getWeightRange(genus, species):
    fishInfo = __fishDict[genus][species]
    return (fishInfo[WEIGHT_MIN_INDEX], fishInfo[WEIGHT_MAX_INDEX])


def getRarity(genus, species):
    return __fishDict[genus][species][RARITY_INDEX]


def getValue(genus, species, weight):
    rarity = getRarity(genus, species)
    rarityValue = pow(RARITY_VALUE_SCALE * rarity, 1.5)
    weightValue = pow(WEIGHT_VALUE_SCALE * weight, 1.1)
    value = OVERALL_VALUE_SCALE * (rarityValue + weightValue)
    finalValue = int(ceil(value))
    base = getBase()
    return finalValue

def getFishDict():
    return __fishDict