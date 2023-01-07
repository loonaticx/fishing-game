from fishbase.EnumBase import *

"""
location enum: [
    "playground name",
    "playground desc",
    "playground color hex for border",
    possibly geerated fish info,
    npc fisherman name
]
"""
LocationInfo = {
    Location.ToontownCentral: [
        "Toontown Central Playground",
        "THIS IS THE TOONTWON CENTRAL PLAYGROUND list stretes here or something",
    ],
    Location.SillyStreet: [
        "SillyStreet"
    ],
    Location.PunchlinePlace: [
        "PunchlinePlace"
    ],
    Location.LoopyLane: [
        "LoopyLane"
    ],

    Location.DonaldsDock: ["Donalds Dock Playground"],
    Location.BarnacleBoulevard: ["BarnacleBoulevard"],
    Location.SeaweedStreet: ["SeaweedStreet"],
    Location.LighthouseLane: ["LighthouseLane"],

    Location.DaisyGardens: ["Daisy Gardens Playground"],
    Location.ElmStreet: ["Elm Street"],
    Location.OakStreet: ["OakStreet"],
    Location.MapleStreet: ["MapleStreet"],

    Location.MinniesMelodyland: ["Minnies Melodyland Playground"],
    Location.AltoAvenue: ["AltoAvenue"],
    Location.TenorTerrace: ["TenorTerrace"],
    Location.BaritoneBoulevard: ["Baritone Boulevard"],

    Location.TheBrrrgh: ["The Brrrgh Playground"],
    Location.PolarPlace: ["Polar Place"],
    Location.WalrusWay: ["Walrus Way"],
    Location.SleetStreet: ["Sleet Street"],

    Location.DonaldsDreamland: ["Donalds Dreamland Playground"],
    Location.LullabyLane: ["Lullaby Lane"],
    Location.PajamaPlace: ["Pajama Place"],

    Location.MyEstate: ["The Estate"],
    Location.OutdoorZone: ["Acorn Acres"],

    None: ["Unknown"]
}


def getLocationName(locationID: Location):
    return LocationInfo.get(locationID)[0]
