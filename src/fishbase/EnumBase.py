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


class ContextStatus(IntEnum):
    UNKNOWN = -1
    LOCKED = 0
    UNLOCKED = 1
