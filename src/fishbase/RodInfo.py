from fishbase.EnumBase import *

GlobalRarityDialBase = 4.3

RodPriceDict = {
    FishingRod.TWIG_ROD: 0,
    FishingRod.BAMBOO_ROD: 400,
    FishingRod.HARDWOOD_ROD: 800,
    FishingRod.STEEL_ROD: 1200,
    FishingRod.GOLD_ROD: 2000
}

Rod2JellybeanDict = {
    FishingRod.TWIG_ROD: 10,
    FishingRod.BAMBOO_ROD: 20,
    FishingRod.HARDWOOD_ROD: 30,
    FishingRod.STEEL_ROD: 75,
    FishingRod.GOLD_ROD: 100
}

# This is how much each rod changes the global rarity dice rolls These get
# multiplied into the GlobalRarityDialBase, thus making the rare fish less
# rare.  The rarity curve is controlled by this exponent in the dict
# below. Making that value smaller (where 1/2 = square root, 1/3 = cube
# root, etc) will make higher rarity levels even harder to find by making
# the curve steeper.
RodRarityFactor = {
    FishingRod.TWIG_ROD: 1.0 / (GlobalRarityDialBase * 1),
    FishingRod.BAMBOO_ROD: 1.0 / (GlobalRarityDialBase * 0.975),
    FishingRod.HARDWOOD_ROD: 1.0 / (GlobalRarityDialBase * 0.95),
    FishingRod.STEEL_ROD: 1.0 / (GlobalRarityDialBase * 0.9),
    FishingRod.GOLD_ROD: 1.0 / (GlobalRarityDialBase * 0.85)
}
MaxRodId = 4

# Indexes into the FishDict data
ROD_WEIGHT_MIN_INDEX = 0
ROD_WEIGHT_MAX_INDEX = 1
ROD_CAST_COST_INDEX = 2

# Rods with their associated weight ranges
# Rods can catch the minimum up to the maximum
rodDict = {
    FishingRod.TWIG_ROD: (0, 4, 1),
    FishingRod.BAMBOO_ROD: (0, 8, 2),
    FishingRod.HARDWOOD_ROD: (0, 12, 3),
    FishingRod.STEEL_ROD: (0, 16, 4),
    FishingRod.GOLD_ROD: (0, 20, 5)
}

FishingRod = "%s Rod"
FishingRodNameDict = {
    0: "Twig",
    1: "Bamboo",
    2: "Hardwood",
    3: "Steel",
    4: "Gold",
}
