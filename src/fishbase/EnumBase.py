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

class SessionMenu(IntEnum):
    # this is to support the back button feature
    NONE = -1
    MAIN_MENU = 0  # pick between playing campaign
    CAMPAIGN_MENU = 1  # in menu explaining campaign
    TUTORIAL_MENU = 2
    LOCATION_MENU = 3  # currently traveling somewhere
    POND_MENU = 4  # currently in the fishing pond menu
    SELL_MENU = 5
    SHOP_MENU = 6
    INVENTORY_MENU = 7


class FishingRod(IntEnum):
    NONE = -1
    TWIG_ROD = 0
    BAMBOO_ROD = 1
    HARDWOOD_ROD = 2
    STEEL_ROD = 3
    GOLD_ROD = 4


class Location(IntEnum):
    NONE = -1
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
    MyEstate = 80

class FishRarity(IntEnum):
    COMMON_MIN = 0  # This isn't a used rarity, just to accommodate.
    COMMON_1 = 1
    COMMON_2 = 2
    UNCOMMON_1 = 3
    UNCOMMON_2 = 4
    UNCOMMON_3 = 5
    RARE_1 = 6
    RARE_2 = 7
    ULTRA_RARE_1 = 8
    ULTRA_RARE_2 = 9
    ULTRA_RARE_3 = 10
    ULTRA_RARE_MAX = 11  # This isn't actually a used rarity, just to accommodate range functions.

class FishGenus(IntEnum):
    NONE = -1
    BALLOON_FISH = 0
    CAT_FISH = 2
    CLOWN_FISH = 4
    FROZEN_FISH = 6
    STAR_FISH = 8
    HOLEY_MACKEREL = 10
    DOG_FISH = 12
    AMORE_EEL = 14
    NURSE_SHARK = 16
    KING_CRAB = 18
    MOON_FISH = 20
    SEA_HORSE = 22
    POOL_SHARK = 24
    BEAR_ACUDA = 26
    CUTTHROAT_TROUT = 28
    PIANO_TUNA = 30
    PBJ_FISH = 32
    DEVIL_RAY = 34


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

    AMORE_EEL = 0
    ELECTRIC_AMORE_EEL = 1

    NURSE_SHARK = 0
    CLARA_NURSE_SHARK = 1
    FLORENCE_NURSE_SHARK = 2

    KING_CRAB = 0
    ALASKAN_KING_CRAB = 1
    OLD_KING_CRAB = 2

    MOON_FISH = 0
    FULL_MOON_FISH = 1
    HALF_MOON_FISH = 2
    NEW_MOON_FISH = 3
    CRESCENT_MOON_FISH = 4
    HARVEST_MOON_FISH = 5

    SEA_HORSE = 0
    ROCKING_SEA_HORSE = 1
    CLYDESDALE_SEA_HORSE = 2
    ARABIAN_SEA_HORSE = 3

    POOL_SHARK = 0
    KIDDIE_POOL_SHARK = 1
    SWIMMING_POOL_SHARK = 2
    OLYMPIC_POOL_SHARK = 3

    BROWN_BEAR = 0
    BLACK_BEAR = 1
    KOALA_BEAR = 2
    HONEY_BEAR = 3
    POLAR_BEAR = 4
    PANDA_BEAR = 5
    KODIAC_BEAR = 6
    GRIZZLY_BEAR = 7

    CUTTHROAT_TROUT = 0
    CAPTAIN_CUTTHROAT_TROUT = 1
    SCURVY_CUTTHROAT_TROUT = 2

    PIANO_TUNA = 0
    GRAND_PIANO = 1
    BABY_GRAND_PIANO = 2
    UPRIGHT_PIANO = 3
    PLAYER_PIANO = 4

    PBJ_FISH = 0
    GRAPE_PBJ_FISH = 1
    CRUNCHY_PBJ_FISH = 2
    STRAWBERRY_PBJ_FISH = 3
    CONCORD_PBJ_FISH = 4

    DEVIL_RAY = 0


class ContextStatus(IntEnum):
    UNKNOWN = -1
    LOCKED = 0
    UNLOCKED = 1
