from enum import IntEnum


class MainMenuChoice(IntEnum):
    NONE = -1
    FISHING_GAME = 0
    FISHING_STATS = 1
    FISHING_AUTOSIM = 2
    FISHING_DEBUG = 4


class GameMode(IntEnum):
    NONE = -1  # go back
    FREE_PLAY = 0
    CAMPAIGN = 1


class FishingRod(IntEnum):
    NONE = -1
    TWIG_ROD = 0
    BAMBOO_ROD = 1
    HARDWOOD_ROD = 2
    STEEL_ROD = 3
    GOLD_ROD = 4


class Location(IntEnum):
    NONE = -1
    TOONTOWN_CENTRAL = 10
    PUNCHLINE_PLACE = 11
    LOOPY_LANE = 12
    SILLY_STREET = 13

    DONALDS_DOCK = 20
    BARNACLE_BOULEVARD = 21
    SEAWEED_STREET = 22
    LIGHTHOUSE_LANE = 23

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

class FishGenus(IntEnum):
    NONE = -1
    BALLOON_FISH = 0
    CAT_FISH = 2
    CLOWN_FISH = 4
    FROZEN_FISH = 6
    STAR_FISH = 8
    HOLEY_MACKEREL = 10

class FishSpecies(IntEnum):
    BALLOON_FISH = 0
    HOT_AIR_BALLOON_FISH = 1
    WEATHER_BALLOON_FISH = 2
    WATER_BALLOON_FISH = 3
    RED_BALLOON_FISH = 4

    CAT_FISH = 0
    SIAMESE = 1
    ALLEY = 2
    TABBY = 3
    TOM = 4

    CLOWN_FISH = 0
    SAD = 1
    PARTY = 2
    CIRCUS = 3

    FROZEN_FISH = 0

    STAR_FISH = 0
    FIVE_STAR_FISH = 1
    ROCK_STAR_FISH = 2
    SHINING_STAR_FISH = 3
    ALL_STAR_FISH = 4

    HOLEY_MACKEREL = 0

    DOG_FISH = 0
    BULL_DOG_FISH = 1
    HOT_DOG_FISH = 2
    DALMATION_DOG_FISH = 3
    PUPPY_DOG_FISH = 4


class ContextStatus(IntEnum):
    UNKNOWN = -1
    LOCKED = 0
    UNLOCKED = 1
