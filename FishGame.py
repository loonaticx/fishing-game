import copy
import FishGameGlobals
import FishLocalizer
import random
from math import ceil, pow


# this file should contain LOGIC but not definitions


"""
pondInfoDict is a version of the fishDict, with zone as the primary key, rod as the secondary key,
with a list of fish (genus, species) and their effecitve rarities at that pond.
{ zone1 : { rod0 : ((genus, species, effectiveRarity), etc)
            rod1 : ((genus, species, effectiveRarity), etc)
            etc
           }
  zone2 : { rod0 : ((genus, species, effectiveRarity), etc)
            rod1 : ((genus, species, effectiveRarity), etc)
            etc
           }
  etc
  }
"""

class FishGame:
    def __init__(self):
        self.globals = FishGameGlobals
        self.pondInfoDict = {}
        self.totalNumFish = 0
        self.emptyRodDict {} # should these be moved into globals... probably tbh
        # actually maybe not for values that r subject to change like totalNumFish
        self.anywhereDict = copy.deepcopy(self.emptyRodDict)
        for rodIndex in self.globals.rodDict:
            self.emptyRodDict[rodIndex] = {}

        fishDict = self.globals.getFishDict()
        self.calculateFishLocations(fishDict)
        pass

    def canBeCaughtByRod(self, genus, species, rodIndex):
        minFishWeight, maxFishWeight = self.globals.getWeightRange(genus, species)
        minRodWeight, maxRodWeight = self.globals.getRodWeightRange(rodIndex)
        if minRodWeight <= maxFishWeight and maxRodWeight >= minFishWeight:
            return 1
        else:
            return 0


    # this code initializes fish locations
    def calculateFishLocations(self, fishDict):
        for genus, speciesList in list(fishDict.items()):
            for species in range(len(speciesList)):
                self.totalNumFish += 1

                # Pull off the properties we are interested in
                speciesDesc = speciesList[species]
                rarity = speciesDesc[self.globals.RARITY_INDEX]
                zoneList = speciesDesc[self.globals.ZONE_LIST_INDEX]

                # Add entries for all the zones this Fish is found in
                for zoneIndex in range(len(zoneList)):
                    # Special case if the fish is found anywhere, store it in a temp
                    # holding dict to be added to the pondInfoDict at the end of all this
                    zone = zoneList[zoneIndex]
                    effectiveRarity = getEffectiveRarity(rarity, zoneIndex)
                    if zone == self.globals.Anywhere:
                        # Now go through the rod indexes adding fish to the pond that
                        # can be caught by that rod
                        for rodIndex, rarityDict in list(self.anywhereDict.items()):
                            if self.canBeCaughtByRod(genus, species, rodIndex):
                                fishList = rarityDict.setdefault(effectiveRarity, [])
                                fishList.append((genus, species))

                    else:
                        # The effective rarity is higher the later the zone is
                        # on the list
                        # Fetch or create the rod dict
                        # Note - we do not use setdefualt here so we do not have to
                        # waste a bunch of copy.deepcopy's of the emptyRodDict
                        pondZones = [zone]
                        for pondZone in pondZones:
                            if pondZone in self.pondInfoDict:
                                rodDict = self.pondInfoDict[pondZone]
                            else:
                                rodDict = copy.deepcopy(self.emptyRodDict)
                                self.pondInfoDict[pondZone] = rodDict

                            # Now go through the rod indexes adding fish to the pond that
                            # can be caught by that rod
                            for rodIndex, rarityDict in list(rodDict.items()):
                                if self.canBeCaughtByRod(genus, species, rodIndex):
                                    fishList = rarityDict.setdefault(
                                        effectiveRarity, [])
                                    fishList.append((genus, species))

        # Now add the fish in the anywhere dict to the pondInfoDict entries
        for zone, rodDict in list(self.pondInfoDict.items()):
            for rodIndex, anywhereRarityDict in list(self.anywhereDict.items()):
                for rarity, anywhereFishList in list(anywhereRarityDict.items()):
                    rarityDict = rodDict[rodIndex]
                    fishList = rarityDict.setdefault(rarity, [])
                    fishList.extend(anywhereFishList)


    def getEffectiveRarity(self, rarity, offset):
        try:
            nerfs = base.cr.nerfsMode
        except:
            nerfs = config.GetBool('nerfs-mode', False)

        if nerfs:
            maxRarity = MAX_RARITY_NERFS
        else:
            maxRarity = MAX_RARITY

        return min(maxRarity, rarity + offset)


    def getPondDict(self, zoneId):
        print(self.pondInfoDict[zoneId])

    def getPondInfo(self):
        return self.pondInfoDict # should be used for fishGameSim display

    def getRodWeightRange(self, rodIndex):
        rodProps = __rodDict[rodIndex]
        return (rodProps[ROD_WEIGHT_MIN_INDEX], rodProps[ROD_WEIGHT_MAX_INDEX])


    def __rollRarityDice(self, rodId, rNumGen):
        """
        Returns a rarity level with proper percent chance of getting that rarity level
        Now we can take the rodId into consideration. This allows us to have the higher
        level rods catch more rare fish
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


    def getRandomWeight(self, genus, species, rodIndex=None, rNumGen=None):
        minFishWeight, maxFishWeight = getWeightRange(genus, species)
        if rodIndex is None:
            minWeight = minFishWeight
            maxWeight = maxFishWeight
        else:
            minRodWeight, maxRodWeight = getRodWeightRange(rodIndex)
            minWeight = max(minFishWeight, minRodWeight)
            maxWeight = min(maxFishWeight, maxRodWeight)
        if rNumGen is None:
            randNumA = random.random()
            randNumB = random.random()
        else:
            randNumA = rNumGen.random()
            randNumB = rNumGen.random()
        randNum = (randNumA + randNumB) / 2.0
        randWeight = minWeight + (maxWeight - minWeight) * randNum
        return int(round(randWeight * 16))


    def getRandomFishVitals(self, zoneId, rodId, rNumGen=None):
        rarity = __rollRarityDice(rodId, rNumGen)
        rodDict = __pondInfoDict.get(zoneId)
        rarityDict = rodDict.get(rodId)
        fishList = rarityDict.get(rarity)
        if fishList:
            if rNumGen is None:
                genus, species = random.choice(fishList)
            else:
                genus, species = rNumGen.choice(fishList)
            weight = getRandomWeight(genus, species, rodId, rNumGen)
            return (1,
                    genus,
                    species,
                    weight)
        else:
            return (0, 0, 0, 0)
        return



def testRarity(rodId=0, numIter=100000):
    d = {1: 0,
         2: 0,
         3: 0,
         4: 0,
         5: 0,
         6: 0,
         7: 0,
         8: 0,
         9: 0,
         10: 0}
    for i in range(numIter):
        v = __rollRarityDice(rodId)
        d[v] += 1

    for rarity, count in list(d.items()):
        percentage = count / float(numIter) * 100
        d[rarity] = percentage

    print(d)


def getRandomFish():
    genus = random.choice(list(__fishDict.keys()))
    species = random.randint(0, len(__fishDict[genus]) - 1)
    return (genus, species)





def getSimplePondInfo():
    info = {}
    for pondId, pondInfo in list(__pondInfoDict.items()):
        pondFishList = []
        for rodId, rodInfo in list(pondInfo.items()):
            for rarity, fishList in list(rodInfo.items()):
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
        if fish[0] not in tmpList:
            tmpList.append(fish[0])
            generaList.append(fish)

    return generaList


def printNumGeneraPerPond():
    pondInfo = getSimplePondInfo()
    for pondId, fishList in list(pondInfo.items()):
        generaList = []
        for fish in fishList:
            if fish[0] not in generaList:
                generaList.append(fish[0])

        print('Pond %s has %s Genera' % (pondId, len(generaList)))


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
    for pond in __pondInfoDict:
        totalPondMoney[pond] = 0
        totalPondBaitCost[pond] = 0
        for rod in range(MaxRodId + 1):
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
                            TTLocalizer.FishSpeciesNames[genus][species], weight, value))
                        totalPondMoney[pond] += value
                        totalRodMoney[rod] += value
                elif itemType == JellybeanItem:
                    value = Rod2JellybeanDict[rod]
                    print("Jellybeans Caught: {}".format(value))
                    totalPondMoney[pond] += value
                    totalRodMoney[rod] += value

    numPonds = len(totalPondMoney)
    for pond, money in list(totalPondMoney.items()):
        baitCost = 0
        for rod in range(MaxRodId + 1):
            baitCost += getCastCost(rod)

        totalCastCost = baitCost * numCasts
        print(('pond: %s  totalMoney: %s profit: %s perCast: %s' % (pond,
                                                                    money,
                                                                    money - totalCastCost,
                                                                    (money - totalCastCost) / float(numCasts * (MaxRodId + 1))),))

    for rod, money in list(totalRodMoney.items()):
        baitCost = getCastCost(rod)
        totalCastCost = baitCost * (numCasts * numPonds)
        print(('rod: %s totalMoney: %s castCost: %s profit: %s perCast: %s' % (rod,
                                                                               money,
                                                                               totalCastCost,
                                                                               money - totalCastCost,
                                                                               (money - totalCastCost) / float(numCasts * numPonds)),))
