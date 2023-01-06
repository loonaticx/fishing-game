import copy
import random
from math import ceil

from fishbase import RodInfo, FishGameGlobals
from fishbase.FishGameGlobals import *
from fishbase.RodInfo import rodDict as __rodDict, RodRarityFactor

fishdict = getFishDict()

def getRodWeightRange(rodIndex):
    """
    Return the min and max weight this rod can handle.
    """
    rodProps = __rodDict[rodIndex]
    # print(len(rodProps))
    # print(rodProps)

    return rodProps[ROD_WEIGHT_MIN_INDEX], rodProps[ROD_WEIGHT_MAX_INDEX]

def getRandomWeight(genus, species, rodIndex = None, rNumGen = None):
    """
    Get a weight value for the fish specified, taking the rod we
    are using into account (if specified). This returns weights that
    have a nice bell curve distribution.
    """
    minFishWeight, maxFishWeight = getWeightRange(genus, species)
    if rodIndex is None:
        # Use the actual fish values unmodified
        minWeight = minFishWeight
        maxWeight = maxFishWeight
    else:
        minRodWeight, maxRodWeight = getRodWeightRange(rodIndex)
        # Clamp the effective fish weight by the amount this rod can handle
        minWeight = max(minFishWeight, minRodWeight)
        maxWeight = min(maxFishWeight, maxRodWeight)

    # Add a few random numbers to give a natural bell curve of probabilities
    if rNumGen is None:
        randNumA = random.random()
        randNumB = random.random()
    else:
        randNumA = rNumGen.random()
        randNumB = rNumGen.random()

    randNum = (randNumA + randNumB) / 2.0
    # Scale the 0-1 values into the effective weight range possible
    randWeight = minWeight + ((maxWeight - minWeight) * randNum)
    # Convert to ounces and round to integer
    return int(round(randWeight * 16))


FishSpeciesNames = {
    0 : ( "Balloon Fish",
          "Hot Air Balloon Fish",
          "Weather Balloon Fish",
          "Water Balloon Fish",
          "Red Balloon Fish",
          ),
    2 : ( "Cat Fish",
          "Siamese Cat Fish",
          "Alley Cat Fish",
          "Tabby Cat Fish",
          "Tom Cat Fish",
          ),
    4 : ( "Clown Fish",
          "Sad Clown Fish",
          "Party Clown Fish",
          "Circus Clown Fish",
          ),
    6 : ( "Frozen Fish",
          ),
    8 : ( "Star Fish",
          "Five Star Fish",
          "Rock Star Fish",
          "Shining Star Fish",
          "All Star Fish",
          ),
    10 : ( "Holey Mackerel",
           ),
    12 : ( "Dog Fish",
           "Bull Dog Fish",
           "Hot Dog Fish",
           "Dalmatian Dog Fish",
           "Puppy Dog Fish",
           ),
    14 : ( "Amore Eel",
           "Electric Amore Eel",
           ),
    16 : ( "Nurse Shark",
           "Clara Nurse Shark",
           "Florence Nurse Shark",
           ),
    18 : ( "King Crab",
           "Alaskan King Crab",
           "Old King Crab",
           ),
    20 : ( "Moon Fish",
           "Full Moon Fish",
           "Half Moon Fish",
           "New Moon Fish",
           "Crescent Moon Fish",
           "Harvest Moon Fish",
           ),
    22 : ( "Sea Horse",
           "Rocking Sea Horse",
           "Clydesdale Sea Horse",
           "Arabian Sea Horse",
           ),
    24 : ( "Pool Shark",
           "Kiddie Pool Shark",
           "Swimming Pool Shark",
           "Olympic Pool Shark",
           ),
    26 : ( "Brown Bear Acuda",
           "Black Bear Acuda",
           "Koala Bear Acuda",
           "Honey Bear Acuda",
           "Polar Bear Acuda",
           "Panda Bear Acuda",
           "Kodiac Bear Acuda",
           "Grizzly Bear Acuda",
           ),
    28 : ( "Cutthroat Trout",
           "Captain Cutthroat Trout",
           "Scurvy Cutthroat Trout",
           ),
    30 : ( "Piano Tuna",
           "Grand Piano Tuna",
           "Baby Grand Piano Tuna",
           "Upright Piano Tuna",
           "Player Piano Tuna",
           ),
    32 : ( "Peanut Butter & Jellyfish",
           "Grape PB&J Fish",
           "Crunchy PB&J Fish",
           "Strawberry PB&J Fish",
           "Concord Grape PB&J Fish",
           ),
    34 : ( "Devil Ray",
           ),
    }

def chooseitem():
    rand = random.random() * 100.0
    for cutoff in SortedProbabilityCutoffs:
        print(f"cutoff - {cutoff}")
        if rand <= cutoff:
            itemType = ProbabilityDict[cutoff]
            # print("__chooseItem: %s" % (itemType))
            return itemType
    print("Somehow we did not choose an item, returning boot")
    return BootItem

def rollRarityDice(rodId, rNumGen):
    """
    Returns a rarity level with proper percent chance of getting that rarity level
    Now we can take the rodId into consideration. This allows us to have the higher
    level rods catch more rare fish

    :param rodId:
    :param rNumGen:
    :return: int [1-6]
    """
    if rNumGen is None:
        diceRoll = random.random()
    else:
        diceRoll = rNumGen.random()

    exp = RodRarityFactor[rodId]
    rarity = int(ceil(10 * (1 - pow(diceRoll, exp))))
    # If random.random() returns exactly 1.0, the math has an edge condition where
    # rarity will equal exactly 0, which is not a valid value, just return 1 instead
    if rarity <= 0:
        rarity = 1
    return rarity

"""
    rarity = __rollRarityDice(rodId, rNumGen)
    rodDict = __pondInfoDict.get(zoneId)
    rarityDict = rodDict.get(rodId)
    fishList = rarityDict.get(rarity)

"""




def canBeCaughtByRod(genus, species, rodIndex):
    minFishWeight, maxFishWeight = getWeightRange(genus, species)
    # print(getRodWeightRange(rodIndex))
    minRodWeight, maxRodWeight = getRodWeightRange(rodIndex)
    # See if the weight ranges overlap. If they do at all, we can
    # catch this fish with this rod
    if ((minRodWeight <= maxFishWeight) and
        (maxRodWeight >= minFishWeight)):
        return 1
    else:
        return 0



__totalNumFish = 0

__emptyRodDict = {}
for rodIndex in __rodDict:
    __emptyRodDict[rodIndex] = {}

__anywhereDict = copy.deepcopy(__emptyRodDict)

__pondInfoDict = {}
def getCastCost(rodId):
    return __rodDict[rodId][ROD_CAST_COST_INDEX]

def getEffectiveRarity(rarity, offset):
    return min(MAX_RARITY, rarity + (offset))

# Loop through all the fish
for genus, speciesList in list(fishdict.items()):
    for species in range(len(speciesList)):
        __totalNumFish += 1
        # Pull off the properties we are interested in
        speciesDesc = speciesList[species]
        rarity = speciesDesc[RARITY_INDEX]
        zoneList = speciesDesc[ZONE_LIST_INDEX]
        # Add entries for all the zones this Fish is found in
        for zoneIndex in range(len(zoneList)):
            # Special case if the fish is found anywhere, store it in a temp
            # holding dict to be added to the pondInfoDict at the end of all this
            zone = zoneList[zoneIndex]
            effectiveRarity = getEffectiveRarity(rarity, zoneIndex)
            if zone == Anywhere:
                # Now go through the rod indexes adding fish to the pond that
                # can be caught by that rod
                for rodIndex, rarityDict in list(__anywhereDict.items()):
                    # print(f"rodINdex = {rodIndex}")
                    if canBeCaughtByRod(genus, species, rodIndex):
                        fishList = rarityDict.setdefault(effectiveRarity, [])
                        fishList.append((genus, species))

            else:
                # The effective rarity is higher the later the zone is
                # on the list
                # Fetch or create the rod dict
                # Note - we do not use setdefualt here so we do not have to
                # waste a bunch of copy.deepcopy's of the emptyRodDict
                pondZones = [zone]
                subZones = HoodHierarchy.get(zone)
                if subZones:
                    pondZones.extend(subZones)
                for pondZone in pondZones:
                    if pondZone in __pondInfoDict:
                        rodDict = __pondInfoDict[pondZone]
                    else:
                        rodDict = copy.deepcopy(__emptyRodDict)
                        __pondInfoDict[pondZone] = rodDict
                    # Now go through the rod indexes adding fish to the pond that
                    # can be caught by that rod
                    for rodIndex, rarityDict in list(rodDict.items()):
                        # print(f"2rodINdex = {rodIndex}")
                        if canBeCaughtByRod(genus, species, rodIndex):
                            fishList = rarityDict.setdefault(effectiveRarity, [])
                            fishList.append((genus, species))

# Now add the fish in the anywhere dict to the pondInfoDict entries
for zone, rodDict in list(__pondInfoDict.items()):
    for rodIndex, anywhereRarityDict in list(__anywhereDict.items()):
        for rarity, anywhereFishList in list(anywhereRarityDict.items()):
            rarityDict = rodDict[rodIndex]
            fishList = rarityDict.setdefault(rarity, [])
            fishList.extend(anywhereFishList)


def getRandomFishVitals(zoneId, rodId, rNumGen=None):
    """
    Returns a random fish, with rarity taken into consideration
    """
    rarity = rollRarityDice(rodId, rNumGen)
    rodDict = __pondInfoDict.get(zoneId)
    # for k in __pondInfoDict.keys():
    #     print(k)
    rarityDict = rodDict.get(rodId)
    fishList = rarityDict.get(rarity)
    # print(rarityDict)
    if fishList:
        if rNumGen is None:
            genus, species = random.choice(fishList)
        else:
            genus, species = rNumGen.choice(fishList)
        weight = getRandomWeight(genus, species, rodId, rNumGen)
        return (1, genus, species, weight)
    else:
        return (0, 0, 0, 0)


def testRarity(rodId = 0, numIter = 100000):
    """
    For debugging only: run this to check the percentage chance of finding
    each rarity level. Prints out a dictionary of the values from simulation.

    :param rodId: 0
    :param numIter: 100000
    """
    d = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
    for i in range(numIter):
        v = rollRarityDice(rodId, None)
        d[v] += 1
    # convert to a percentage
    for rarity, count in list(d.items()):
        percentage = count / float(numIter) * 100
        d[rarity] = percentage
    return d

def generateFishingReport(numCasts=10000, hitRate=0.8):  # hitrate = fail catch?
    # THIS INCLUDES EVERY SINGLE ZONE
    """
    Prints out a report from a full simulation of the fishing
    system, including boots, jellybean bonuses, and the cost of casting.
    Shows profit per rod and per pond.

    hitRate is how often the user hits a fish
    hitRate of 1.0 means you always hit, 0.5 means half the time
    """
    totalPondMoney = {}
    totalRodMoney = {}
    totalPondBaitCost = {}
    pondData = []
    rodData = []

    for pond in __pondInfoDict:
        totalPondMoney[pond] = 0
        totalPondBaitCost[pond] = 0
        for rod in range(RodInfo.MaxRodId + 1):
            totalRodMoney.setdefault(rod, 0)
            baitCost = getCastCost(rod)
            for cast in range(numCasts):
                totalPondBaitCost[pond] += baitCost
                if random.random() > hitRate:
                    continue
                rand = random.random() * 100.0
                for cutoff in SortedProbabilityCutoffs:
                    if rand <= cutoff:
                        itemType = ProbabilityDict[cutoff]
                        break

                if itemType == FishItem:
                    success, genus, species, weight = getRandomFishVitals(
                        pond, rod)
                    if success:
                        value = getValue(genus, species, weight)
                        print("Fish: {}, Weight: {}, Value: {}".format(
                            FishLocalizer.FishSpeciesNames[genus][species], weight, value))
                        totalPondMoney[pond] += value
                        totalRodMoney[rod] += value
                elif itemType == JellybeanItem:
                    value = RodInfo.Rod2JellybeanDict[rod]
                    print("Jellybeans Caught: {}".format(value))
                    totalPondMoney[pond] += value
                    totalRodMoney[rod] += value

    numPonds = len(totalPondMoney)
    for pond, money in list(totalPondMoney.items()):
        baitCost = 0
        for rod in range(RodInfo.MaxRodId + 1):
            baitCost += getCastCost(rod)

        totalCastCost = baitCost * numCasts
        pondData.append(f"pond: {pond} totalMoney: {money} Profit:{money - totalCastCost} perCast: {(money - totalCastCost) / float(numCasts * (RodInfo.MaxRodId + 1))}")

    for rod, money in list(totalRodMoney.items()):
        baitCost = getCastCost(rod)
        totalCastCost = baitCost * (numCasts * numPonds)
        rodData.append(f"rod: {rod} totalMoney: {money} castCost: {totalCastCost} profit: {money-totalCastCost} perCast: {(money - totalCastCost) / float(numCasts * numPonds)}")

    return pondData, rodData

def getPondInfo():
    # This looks best when pprinted
    # import pprint
    # pprint.pprint(FishGlobals.getPondInfo())
    return __pondInfoDict

def getSimplePondInfo():
    # This looks best when pprinted
    # import pprint
    # pprint.pprint(FishGlobals.getPondInfo())
    info = {}
    for pondId, pondInfo in __pondInfoDict.items():
        pondFishList = []
        for rodId, rodInfo in pondInfo.items():
            for rarity, fishList in rodInfo.items():
                for fish in fishList:
                    if fish not in pondFishList:
                        pondFishList.append(fish)
        pondFishList.sort()
        info[pondId] = pondFishList
    return info

def getPondGeneraList(pondId):
    tmpList = []
    generaList = []
    pondInfo = getSimplePondInfo()
    for fish in pondInfo[pondId]:
        # todo: convert this to set
        if fish[0] not in tmpList:
            tmpList.append( fish[0] )
            generaList.append( fish )
    return generaList

def getPondGeneraListNames(pondId):
    generaList = getPondGeneraList(pondId)
    genusNames = []
    # doesnt actually generate species, only genera
    for genus, species in FishSpeciesNames[generaList]:
        pass
    # idk im too sleepy to finish this one sorry
    # return genus

# print(__pondInfoDict)

# for i in range(10000):
#     _, genus, species, weight = getRandomFishVitals(zoneId=16000, rodId=FishingRod.TWIG_ROD)
#     print(f"{FishSpeciesNames[genus][species]} : {genus}, {species}")
#
# for genus in fishdict.keys():
#     for fish_species in FishSpeciesNames[genus]:
#         # for item in fishdict[genus]:
#         #     print(item)
#         # f = fishdict[genus][0]
#         # weight_min = f[0]
#         # print(weight_min)
#         # weight_max = f[1]
#         # rarity = f[2]
#         # zone_list= f[3]
#         weight_min, weight_max, rarity, zone_list = fishdict[genus][0]
#         # print(f"{fish_species}: {fishdict[genus]}")