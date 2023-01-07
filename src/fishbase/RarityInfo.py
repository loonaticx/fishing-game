from fishbase.EnumBase import FishRarity as FR

RARITY_COMMON = (FR.COMMON_MIN, FR.COMMON_1, FR.COMMON_2)
RARITY_UNCOMMON = (FR.UNCOMMON_1, FR.UNCOMMON_2, FR.UNCOMMON_3)
RARITY_RARE = (FR.RARE_1, FR.RARE_2)
RARITY_ULTRA_RARE = (FR.ULTRA_RARE_1, FR.ULTRA_RARE_2, FR.ULTRA_RARE_3, FR.ULTRA_RARE_MAX)

# i know, this is a me-lame way of doing it. whatever
RarityIndex = {None: ["Unknown", "#9C9C9C"]}
def generateRarityIndex():
    for rarity in RARITY_COMMON:
        RarityIndex[rarity] = ["Common", "#7cd17a"]
    for rarity in RARITY_UNCOMMON:
        RarityIndex[rarity] = ["Uncommon", "#58AAE2"]
    for rarity in RARITY_RARE:
        RarityIndex[rarity] = ["Rare", "#EC3A31"]
    for rarity in RARITY_ULTRA_RARE:
        RarityIndex[rarity] = ["Ultra Rare", "#EBF425"]


generateRarityIndex()
