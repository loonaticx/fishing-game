from fishbase.EnumBase import FishingRod
from fishbase.RodInfo import RodPriceDict, RodRarityFactor, Rod2JellybeanDict

MainMenuItems = [
    ("Play Fishing Game", "Description about Fishing Game"),
    ("Review Fish Statistics", "Description about that"),
    # give x amount of trials and generate results
    ("Simulate Fishing", "Description"),
    ("Debug Fishing", "debug")
]

MenuGameModeItems = [
    ("Free Play", "Description about Free Play"),
    ("Campaign", "Description about Campaign"),
    ("Back", "Go back to Main Menu")  # always have this entry last
    # ("AutoSim", "Description about AutoSim")
]

FishermanMenuItems = [
    ("Sell", "Sell your fish here"),
    ("Buy", "Purchase better fishing rods here"),
    ("Tutorial", "Revisit the fishing tutorial"),
    ("Back", "Go Back")
]

RodMenuItems = [
    (
        "Twig",
        "Looks like a bunch of tree branches glued together.",
        f"{RodPriceDict[FishingRod.TWIG_ROD]} Jellybeans",  # Cost
        ## Unlockable Stats ##
        f"{RodRarityFactor[FishingRod.TWIG_ROD]}",  # Rarity Factor
        f"{Rod2JellybeanDict[FishingRod.TWIG_ROD]} Jellybeans",  # Amount from catching Jellybeans
    ),
    ("Bamboo", "Purchase better fishing rods here"),
    ("Hardwood", "Revisit the fishing tutorial"),
    ("Back", "Go Back")
]
