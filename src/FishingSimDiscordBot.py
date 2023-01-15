from typing import Optional, List

import discord
from discord import app_commands
from discord.ext import commands

from fishbase import RodInfo, LocationInfo
from fishbase.FishContext import FishContext
from fishbase.FishContext import FishInternal

import DatabaseManager
# from fishbase.EnumBase import *
from fishbase.FishGameGlobals import getFishDict
from fishbase.RarityInfo import RARITY_COMMON, RARITY_UNCOMMON, RARITY_RARE, RARITY_ULTRA_RARE, RarityIndex
from fishbase.RodInfo import *
import random
from config import config
from testing import fishaccess as FishSim

# GUILDS = [
#     discord.Object(id = config.BOT_GUILDS[0]),
#     discord.Object(id = config.BOT_GUILDS[1]),
#
# ]
# MY_GUILD = GUILDS
from testing.fishaccess import FishSpeciesNames

MY_GUILD = discord.Object(id = config.BOT_GUILD)  # replace with your guild id

ALL_SERVERS = True


class FishingSimBot(commands.Bot):

    def __init__(self, intents, command_prefix, description):
        super().__init__(intents = intents, command_prefix = command_prefix, description = description)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        if ALL_SERVERS:
            await self.tree.sync()
        else:
            self.tree.copy_global_to(guild = MY_GUILD)
            await self.tree.sync(guild = MY_GUILD)


intents = discord.Intents.default()
intents.message_content = True  # required for dropdown

bot = FishingSimBot(command_prefix = '/', description = 'blah', intents = intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.competing, name = "fish gaming"))


class MainMenuButton(discord.ui.Button['MasterView']):
    def __init__(self, game_mode: GameMode, label, style = discord.ButtonStyle.secondary):
        super().__init__(style = style, label = label)
        self.mode = game_mode

    async def callback(self, interaction: discord.Interaction):
        # the function that edits the message
        assert self.view is not None
        view: MasterView = self.view
        if not view.is_host(interaction.user.id):
            await interaction.response.send_message("Sorry, this is not your game.", ephemeral = True)
            return

        view.context.GAME_MODE = self.mode
        view.clear_items()

        files = []

        if view.context.GAME_MODE == GameMode.CAMPAIGN:
            # first time dialogue:
            intro = """
            In this mode, you must work your way up to the top, unlocking rods and playgrounds as you progress.
            """
            em = discord.Embed(
                title = "Welcome to campaign mode!",
                description = str(f"{intro}"),
            )
            em.add_field(name = "Toontown Central", value = f"12 out of 39")
            em.add_field(name = "Total Species", value = f"0 out of 60")
            em.set_author(name="Campaign")

            view.location_options(Location.NONE)
        elif view.context.GAME_MODE == GameMode.FREE_PLAY:
            # free play gives access to everything, has data separate from campaign
            em = discord.Embed(
                title = "Select Playground",
                description = str(f"gm = {view.context.GAME_MODE} - intended {GameMode.CAMPAIGN}"),
            )
            em.add_field(name = "Toontown Central", value = f"12 out of 39")
            em.add_field(name = "Donalds Dock", value = f"12 out of 32")
            em.add_field(name = "Daisy Gardens", value = f"12 out of 23")
            em.add_field(name = "Minnies Melodyland", value = f"9 out of 10")
            em.add_field(name = "The Brrrgh", value = f"12 out of 18")
            em.add_field(name = "Donalds Dreamland", value = f"20 out of 29")
            em.add_field(name = "Acorn Acres", value = f"9 out of 13")
            em.add_field(name = "The Estate", value = f"10 out of 18")
            em.add_field(name = "Total Species", value = f"57 out of 60")

            view.location_options(Location.NONE)
        else:
            em = discord.Embed(
                title = "Select street for nw",
                description = str(f"gm = {view.context.GAME_MODE} - intended {GameMode.CAMPAIGN}"),
            )
            view.location_options(Location.ToontownCentral)

        await interaction.response.edit_message(embed = em, view = view, attachments=files)


# relevant to campaign mode
class TutorialButton(discord.ui.Button['MasterView']):
    def __init__(self, label, style = discord.ButtonStyle.green):
        super().__init__(style = style, label = label)

    async def callback(self, interaction: discord.Interaction):
        # the function that edits the message
        assert self.view is not None
        view: MasterView = self.view
        if not view.is_host(interaction.user.id):
            await interaction.response.send_message("Sorry, this is not your game.", ephemeral = True)
            return

        view.clear_items()

        em = discord.Embed(
            title = "Fisherman Freddy",
            description = f"Why hello there, Toon! Flippy told me that you're the new FisherToon in town.",
        )
        # can colorize these based off rarity
        em.add_field(name="Total Jellybeans", value=view.context.JELLYBEANS_TOTAL)
        em.set_author(name="Campaign - Tutorial")
        view.fisherman_options()
        # remove empty attachment list later
        await interaction.response.edit_message(embed = em, view = view, attachments = [])


class FishHereButton(discord.ui.Button['MasterView']):
    # this is here ONLY TO ENTER THE FISHING MENU
    def __init__(self, label = "Go Fishing!", style = discord.ButtonStyle.red):
        super().__init__(style = style, label = label)

    async def callback(self, interaction: discord.Interaction):
        # the function that edits the message
        assert self.view is not None
        view: MasterView = self.view
        if not view.is_host(interaction.user.id):
            await interaction.response.send_message("Sorry, this is not your game.", ephemeral = True)
            return

        view.clear_items()

        if view.context.BUCKET_SIZE == 0:
            delta_profit = 0
        else:
            # idk
            delta_profit = 0
            # delta_profit = view.context.JELLYBEANS_TOTAL - view.context.JELLYBEANS_CURRENT

        view.context.SESSION_MENU = SessionMenu.POND_MENU

        # if i wanted to be ambitious i could take pictures of areas n set them as images

        em = discord.Embed(
            title = "Ready to fish!",
            description = str(f"uhh probably a list of all the first that can be caught here"),
        )

        if view.context.USE_FISHING_BUCKET:
            em.add_field(name = "Fishing Bucket", value = f"{view.context.BUCKET_SIZE}/{view.context.BUCKET_SIZE_MAX}")
        em.add_field(name = "Total Jellybeans", value = f"{view.context.JELLYBEANS_TOTAL}")
        if view.context.USE_FISHING_BUCKET:
            em.add_field(name = "Fishing Bucket Value", value = f"{view.context.JELLYBEANS_CURRENT}" + " (%+d)" % delta_profit)
        # em.add_field(name = "Fish Bingo?", value = f"No")

        em.set_footer(text = f"Selected Rod: {FishingRodNameDict[view.context.ROD_ID]} | Current Location: {LocationInfo.getLocationName(view.context.LOCATION_ID)}")

        randomfish = f"fish_{random.randint(1, 5)}.png"
        thumbnail = discord.File(f"img/{randomfish}", filename = randomfish)
        em.set_thumbnail(url = f"attachment://{randomfish}")

        view.fish_options()
        await interaction.response.edit_message(embed = em, view = view, attachments = [thumbnail])


class FishButton(discord.ui.Button['MasterView']):
    def __init__(self, label = "Cast", style = discord.ButtonStyle.red, disabled=False, full=False, poor=False):
        if full:
            label = "Bucket Full!"
            style = discord.ButtonStyle.gray
            disabled = True
        elif poor:
            label = "Not enough Jellybeans!"
            style = discord.ButtonStyle.gray
            disabled = True
        super().__init__(style = style, label = label, disabled=disabled)

    async def callback(self, interaction: discord.Interaction):
        # do our initial housekeeping:
        assert self.view is not None
        view: MasterView = self.view
        if not view.is_host(interaction.user.id):
            await interaction.response.send_message("Sorry, this is not your game.", ephemeral = True)
            return

        view.clear_items()
        # ok, user has pressed the button. let's do some calculations.
        zoneId = view.context.LOCATION_ID
        rodId = view.context.ROD_ID
        _, genus, species, weight = FishSim.getRandomFishVitals(zoneId, rodId)
        # todo: check to see if old boot was caught
        caughtFish = FishSim.FishSpeciesNames[genus][species]  # type: str
        fishValue = FishSim.getValue(genus, species, weight)
        profit = fishValue - RodInfo.rodDict[view.context.ROD_ID][2]
        # not sure if this should be locked to campaign or not, for now we will just give it this value
        if view.context.USE_FISHING_BUCKET:
            view.context.JELLYBEANS_TOTAL -= RodInfo.rodDict[view.context.ROD_ID][2]
            view.context.JELLYBEANS_CURRENT += fishValue
            # add the fish to the bucket now
            view.context.BUCKET_CONTENTS.append(
                [caughtFish, weight, fishValue]
            )
        else:
            # Lazy shortcut so that we dont need to call the db twice for casting
            view.context.JELLYBEANS_TOTAL += profit

        # add the fish into our inventory
        view.context.register_fish_record(genus, species, weight)

        # add one to our current session counter
        view.context.CAUGHT_FISH_SESSION += 1

        weight_lowest, weight_highest = view.context.FISH_DATA[genus][species][0]

        rarity = FishSim.fishdict[genus][species][2]
        rarity_desc, color = RarityIndex[rarity]

        extra = ""
        if view.context.NEW_SPECIES:
            extra += "\n**NEW SPECIES!**"
            color = "#98ff48"
        # meh lets not show both new species and record rn since its a bit redundant
        elif view.context.NEW_RECORD:
            extra += "\n**NEW RECORD!!**"
            color = "#98c0ff"

        border = discord.Color.from_str(color)

        image = discord.File(f"img/tt_fish_{genus}.gif", filename = f"tt_fish_{genus}.gif")

        em = discord.Embed(
            title = f"Caught: {caughtFish}",
            description = str(f"{extra}"),
            color = border
        )
        em.add_field(name = "Rarity", value = f"{rarity}/{FishRarity.ULTRA_RARE_MAX - 1} ({rarity_desc})")
        em.add_field(name = "Weight", value = f"{weight} oz\n[L: {weight_lowest} oz, H: {weight_highest} oz]")

        totValue = f"{view.context.JELLYBEANS_TOTAL}"
        if view.context.USE_FISHING_BUCKET:
            em.add_field(
                name = "Fishing Bucket",
                value = f"{view.context.BUCKET_SIZE}/{view.context.BUCKET_SIZE_MAX}"
            )
            em.add_field(name = "Fishing Bucket Value", value = f"{view.context.JELLYBEANS_CURRENT}")
        else:
            # + or - if profit
            totValue += " (%+d)" % profit

        em.add_field(name = "Jellybean Amount", value = f"{fishValue}" + " *(%+d)*" % profit)
        em.add_field(name = "Total Jellybeans", value = totValue)

        em.set_footer(text = f"Selected Rod: {FishingRodNameDict[view.context.ROD_ID]} | Current Location: {LocationInfo.getLocationName(view.context.LOCATION_ID)}"
                             f" | Fish Caught in Session: {view.context.CAUGHT_FISH_SESSION}")
        em.set_image(url = f"attachment://tt_fish_{genus}.gif")

        randomfish = f"fish_{random.randint(1, 5)}.png"
        thumbnail = discord.File(f"img/{randomfish}", filename = randomfish)
        em.set_thumbnail(url = f"attachment://{randomfish}")

        # is our bucket full now?
        view.context.BUCKET_FULL = view.context.BUCKET_SIZE >= view.context.BUCKET_SIZE_MAX

        view.fish_options()
        await interaction.response.edit_message(attachments = [image, thumbnail], embed = em, view = view)


class VisitFishermanButton(discord.ui.Button['MasterView']):
    def __init__(self, label, style = discord.ButtonStyle.green):
        super().__init__(style = style, label = label)

    async def callback(self, interaction: discord.Interaction):
        # the function that edits the message
        assert self.view is not None
        view: MasterView = self.view
        if not view.is_host(interaction.user.id):
            await interaction.response.send_message("Sorry, this is not your game.", ephemeral = True)
            return

        view.clear_items()

        view.context.SESSION_MENU = SessionMenu.SELL_MENU

        npcImage = f"npc_{view.context.LOCATION_ID}.png"

        image = discord.File(f"img/{npcImage}", filename = f"{npcImage}")

        em = discord.Embed(
            title = "FISHERMAN FREDDY",
            description = str(f"no way im fisherman freddy"),
        )
        # can colorize these based off rarity
        # todo: make this look better
        if view.context.USE_FISHING_BUCKET:
            report = "%s\n" % ([name for name in [name for name, something, another in view.context.BUCKET_CONTENTS]])
            em.add_field(name="Fishing Bucket",value=report)

        em.set_thumbnail(url=f"attachment://{npcImage}")
        view.fisherman_options()
        # remove empty attachment list later
        await interaction.response.edit_message(embed = em, view = view, attachments = [image])


class ShopButton(discord.ui.Button['MasterView']):
    def __init__(self, label, style = discord.ButtonStyle.green):
        super().__init__(style = style, label = label)

    async def callback(self, interaction: discord.Interaction):
        # the function that edits the message
        assert self.view is not None
        view: MasterView = self.view
        if not view.is_host(interaction.user.id):
            await interaction.response.send_message("Sorry, this is not your game.", ephemeral = True)
            return

        view.clear_items()

        view.context.SESSION_MENU = SessionMenu.SHOP_MENU

        em = discord.Embed(
            title = "Fishing Shop",
            description = "what the heck is on sale today",
        )
        view.shop_options()
        # remove empty attachment list later
        await interaction.response.edit_message(embed = em, view = view, attachments = [])


class ViewRecordsButton(discord.ui.Button['MasterView']):
    """
    view users fishing records
    """
    def __init__(self, label="View Fishing Records", style = discord.ButtonStyle.green):
        super().__init__(style = style, label = label)

    async def callback(self, interaction: discord.Interaction):
        # the function that edits the message
        assert self.view is not None
        view: MasterView = self.view
        if not view.is_host(interaction.user.id):
            await interaction.response.send_message("Sorry, this is not your game.", ephemeral = True)
            return

        view.clear_items()

        view.context.SESSION_MENU = SessionMenu.RECORDS_MENU

        ##

        recordDisplay = {

        }
        # shouldnt be here but just prototyping? idk
        # build fish record for user ????? idk what i wanna do rn
        fishDict = getFishDict()
        for fishGenus in fishDict.keys():
            # FishSpeciesNames[fishGenus] --> ("species_name_1", "species_name_2",) etc
            friendly_name_genus = FishSpeciesNames[fishGenus][0]  # just take the first entry of the species tuple
            # does player have any register of this fish genus?
            if not view.context.FISH_DATA.get(fishGenus):
                recordDisplay[friendly_name_genus] = ['???']
                continue
            else:
                recordDisplay[friendly_name_genus] = dict()  # dict for each genus (fish type)

            for fishSpecies in fishDict[fishGenus]:
                # ok so we should have this genus if we've got here
                # ok, what about particular fish?
                if view.context.FISH_DATA.get(fishGenus).get(fishSpecies):
                    recordDisplay[friendly_name_genus][fishSpecies] = [f'{FishSpeciesNames[fishGenus][fishSpecies]}']
                else:
                    recordDisplay[friendly_name_genus][fishSpecies] = ['???']

        ##

        em = discord.Embed(
            title = "Fishing Records",
            description = f"{recordDisplay}",
        )
        view.inventory_options()
        # remove empty attachment list later
        await interaction.response.edit_message(embed = em, view = view, attachments = [])

#
class SellButton(discord.ui.Button['MasterView']):
    def __init__(self, label="Sell Fish", style = discord.ButtonStyle.green, disabled=False):
        super().__init__(style = style, label = label, disabled=disabled)

    async def callback(self, interaction: discord.Interaction):
        # TODO: make this not a copy and paste of fishermanbutton
        # the function that edits the message
        assert self.view is not None
        view: MasterView = self.view
        if not view.is_host(interaction.user.id):
            await interaction.response.send_message("Sorry, this is not your game.", ephemeral = True)
            return

        view.clear_items()

        view.context.SESSION_MENU = SessionMenu.SELL_MENU

        # sell the fish and add it to our total jellybeans
        view.context.JELLYBEANS_TOTAL += view.context.JELLYBEANS_CURRENT

        image = discord.File(f"img/Jar_1.png", filename = f"Jar_1.png")

        em = discord.Embed(
            title = f"Thanks! The Pet Shop will love these!",
            description = f"Sweet! You've earned **{view.context.JELLYBEANS_CURRENT} Jellybeans** from your bucket!",
        )
        em.add_field(name = "Total Jellybeans", value = f"{view.context.JELLYBEANS_TOTAL}")
        em.set_thumbnail(url="attachment://Jar_1.png")

        view.context.JELLYBEANS_CURRENT = 0
        view.context.BUCKET_CONTENTS = []
        view.context.BUCKET_FULL = False

        view.fisherman_options()
        # remove empty attachment list later
        await interaction.response.edit_message(embed = em, view = view, attachments = [image])


class UpgradeButton(discord.ui.Button['MasterView']):
    def __init__(self, label, style = discord.ButtonStyle.green):
        super().__init__(style = style, label = label)

    async def callback(self, interaction: discord.Interaction):
        # the function that edits the message
        assert self.view is not None
        view: MasterView = self.view
        if not view.is_host(interaction.user.id):
            await interaction.response.send_message("Sorry, this is not your game.", ephemeral = True)
            return

        view.clear_items()

        em = discord.Embed(
            title = "Fishing Shop",
            description = "what the heck is on sale today",
        )
        view.shop_options()
        # remove empty attachment list later
        await interaction.response.edit_message(embed = em, view = view, attachments = [])


class InventoryButton(discord.ui.Button['MasterView']):
    def __init__(self, label, style = discord.ButtonStyle.green):
        super().__init__(style = style, label = label)

    async def callback(self, interaction: discord.Interaction):
        # the function that edits the message
        assert self.view is not None
        view: MasterView = self.view
        if not view.is_host(interaction.user.id):
            await interaction.response.send_message("Sorry, this is not your game.", ephemeral = True)
            return

        view.clear_items()

        em = discord.Embed(
            title = "Fishing Inventory",
            description = f"Equipped Rod: **{FishingRodNameDict[view.context.ROD_ID]}**",
        )
        # {:.2f
        chance = (((1 / RodRarityFactor[view.context.ROD_ID]) / GlobalRarityDialBase) * 100)
        em.add_field(name="Rod Rarity Chance", value=f"+{abs((chance - 100)):.2f}%")
        em.add_field(name="Rod Price (Jellybeans)", value=RodPriceDict[view.context.ROD_ID])

        rodinfo = rodDict[view.context.ROD_ID]
        em.add_field(name="Fish Weight", value=f"Min: {rodinfo[0]}\nMax: {rodinfo[1]}")
        em.add_field(name="Rod Cast Cost", value=rodinfo[2])


        view.inventory_options()
        # remove empty attachment list later
        await interaction.response.edit_message(embed = em, view = view, attachments = [])


class BackButton(discord.ui.Button['MasterView']):
    def __init__(self, label = "Go Back", style = discord.ButtonStyle.gray):
        super().__init__(style = style, label = label)

    async def callback(self, interaction: discord.Interaction):
        # the function that edits the message
        assert self.view is not None
        view: MasterView = self.view
        if not view.is_host(interaction.user.id):
            await interaction.response.send_message("Sorry, this is not your game.", ephemeral = True)
            return

        view.clear_items()
        # ok, first thing we need to do is see what we're doing:
        # check to see if we've selected a game mode.

        # are we currently selling fish? return to main fish panel

        # are we currently in main fish panel? return to last location

        # if location id is none, what do?
        view.location_options(view.context.LOCATION_ID)
        await interaction.response.edit_message(embed = None, view = view)


class LocationButton(discord.ui.Button['MasterView']):
    """
    Upon clicking on this button, the player will enter a "Location" state.
    """
    # maybe location buttons can light up green if theyve caught all the possible fish for that area
    def __init__(self, location: Location, label="", style = discord.ButtonStyle.blurple):
        if not label:
            label = LocationInfo.LocationInfo[location][0]
        super().__init__(style = style, label = label)
        self.location = location

    async def callback(self, interaction: discord.Interaction):
        # the function that edits the message
        assert self.view is not None
        view: MasterView = self.view
        if not view.is_host(interaction.user.id):
            await interaction.response.send_message("Sorry, this is not your game.", ephemeral = True)
            return
        view.clear_items()

        view.context.LOCATION_ID = self.location
        view.context.SESSION_MENU = SessionMenu.LOCATION_MENU

        files = []

        # We're arriving to a playground
        # eventually: name, desc, color = LocationInfo[blah]
        locationInfo = LocationInfo.LocationInfo[view.context.LOCATION_ID]
        # can include all possible fish you can catch here
        em = discord.Embed(
            title = locationInfo[0],
            description = str(f"THIS IS THE PLAYGROUND list stretes here or something"),
        )
        em.add_field(name="Possible Fish", value=FishSim.getPondGeneraList(view.context.LOCATION_ID))
        view.location_options(view.context.LOCATION_ID)
        await interaction.response.edit_message(embed = em, view = view, attachments=files)


class FishingRodDropdown(discord.ui.Select['MasterView']):
    def __init__(self):
        # in campaign mode we can modify options to show only acquired rods

        # Set the options that will be presented inside the dropdown
        options = []
        for rod in FishingRodNameDict.keys():
            options.append(
                discord.SelectOption(label=FishingRodName % FishingRodNameDict[rod], value=rod, description='Cast: 1 Jellybean', emoji='🟥'),
            )

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select your fishing rod.', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.

        assert self.view is not None
        view: MasterView = self.view
        if not view.is_host(interaction.user.id):
            await interaction.response.send_message("Sorry, this is not your game.", ephemeral = True)
            return
        view.clear_items()

        # Equip our rod by registering it with our FishContext blob.
        self.view.context.ROD_ID = id2Enum[int(self.values[0])]

        em = discord.Embed(
            title = "Fishing Inventory",
            description = f"Equipped Rod: **{FishingRodNameDict[view.context.ROD_ID]}**",
        )
        # (1 / i) / r
        chance = (((1 / RodRarityFactor[view.context.ROD_ID]) / GlobalRarityDialBase) * 100)

        em.add_field(name="Rod Rarity Chance", value=f"+{abs((chance - 100)):.2f}%")
        em.add_field(name="Rod Price", value=RodPriceDict[view.context.ROD_ID])

        rodinfo = rodDict[view.context.ROD_ID]
        em.add_field(name="Fish Weight", value=f"Min: {rodinfo[0]}, Max: {rodinfo[1]}")
        em.add_field(name="Rod Cast Cost", value=rodinfo[2])
        em.add_field(name="Fish Caught w/ Rod", value=str(0))

        rodpicture = f"rod_{view.context.ROD_ID}.png"
        thumbnail = discord.File(f"img/{rodpicture}", filename = rodpicture)
        em.set_thumbnail(url = f"attachment://{rodpicture}")

        view.inventory_options()
        # Re-load the inventory view to show our changes.
        await interaction.response.edit_message(view=view, embed=em, attachments = [thumbnail])


class FishListDropdown(discord.ui.Select['MasterView']):
    def __init__(self):
        # in campaign mode we can modify options to show only acquired rods

        # Set the options that will be presented inside the dropdown
        options = []
        for rod in FishingRodNameDict.keys():
            options.append(
                discord.SelectOption(label=FishingRodName % FishingRodNameDict[rod], value=rod, description='Cast: 1 Jellybean', emoji='🟥'),
            )

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select your fishing rod.', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.

        assert self.view is not None
        view: MasterView = self.view
        if not view.is_host(interaction.user.id):
            await interaction.response.send_message("Sorry, this is not your game.", ephemeral = True)
            return
        view.clear_items()

        # Equip our rod by registering it with our FishContext blob.
        self.view.context.ROD_ID = id2Enum[int(self.values[0])]

        em = discord.Embed(
            title = "Fishing Inventory",
            description = f"Equipped Rod: **{FishingRodNameDict[view.context.ROD_ID]}**",
        )
        # (1 / i) / r
        chance = (((1 / RodRarityFactor[view.context.ROD_ID]) / GlobalRarityDialBase) * 100)

        em.add_field(name="Rod Rarity Chance", value=f"+{abs((chance - 100)):.2f}%")
        em.add_field(name="Rod Price", value=f"{RodPriceDict[view.context.ROD_ID]} Jellybeans")

        rodinfo = rodDict[view.context.ROD_ID]
        em.add_field(name="Fish Weight", value=f"Min: {rodinfo[0]}, Max: {rodinfo[1]}")
        em.add_field(name="Rod Cast Cost", value=f"{rodinfo[2]} Jellybeans")
        em.add_field(name="Fish Caught", value=str(3243))

        view.inventory_options()
        # Re-load the inventory view to show our changes.
        await interaction.response.edit_message(view=view, embed=em)


class MasterView(discord.ui.View):
    LocationButtons = {
        # maybe if player completes all fish for a certain street, they can visit that street from another
        # ex: loopy --> punchline
        # this would require us to change from lists to sets
        Location.NONE: [
            LocationButton(Location.ToontownCentral),
            LocationButton(Location.DonaldsDock),
            LocationButton(Location.DaisyGardens),
            LocationButton(Location.MinniesMelodyland),
            LocationButton(Location.TheBrrrgh),
            LocationButton(Location.DonaldsDreamland),
            LocationButton(Location.MyEstate),
        ],
        Location.ToontownCentral: [
            LocationButton(Location.PunchlinePlace),
            LocationButton(Location.LoopyLane),
            LocationButton(Location.SillyStreet),
            LocationButton(Location.MyEstate),
        ],
        Location.PunchlinePlace: [
            LocationButton(Location.BarnacleBoulevard),
            LocationButton(Location.ToontownCentral),
        ],
        Location.SillyStreet: [
            LocationButton(Location.ElmStreet),
            LocationButton(Location.ToontownCentral),
        ],
        Location.LoopyLane: [
            LocationButton(Location.AltoAvenue),
            LocationButton(Location.ToontownCentral),
        ],
        Location.DonaldsDock: [
            LocationButton(Location.BarnacleBoulevard),
            LocationButton(Location.SeaweedStreet),
            LocationButton(Location.LighthouseLane),
            # LocationButton(Location.OutdoorZone),
        ],
        Location.BarnacleBoulevard: [
            LocationButton(Location.PunchlinePlace),
            LocationButton(Location.DonaldsDock),
        ],
        Location.SeaweedStreet: [
            LocationButton(Location.MapleStreet),
            LocationButton(Location.DonaldsDock),

        ],
        Location.LighthouseLane: [
            LocationButton(Location.WalrusWay),
            LocationButton(Location.DonaldsDock),

        ],
        Location.DaisyGardens: [
            LocationButton(Location.ElmStreet),
            LocationButton(Location.OakStreet),
            LocationButton(Location.MapleStreet),
        ],

        Location.ElmStreet: [
            LocationButton(Location.SillyStreet),
            LocationButton(Location.DaisyGardens),

        ],
        Location.OakStreet: [
            # SBHQ
            LocationButton(Location.DaisyGardens),
        ],
        Location.MapleStreet: [
            LocationButton(Location.SeaweedStreet),
            LocationButton(Location.DaisyGardens),
        ],
        Location.MinniesMelodyland: [
            LocationButton(Location.AltoAvenue),
            LocationButton(Location.BaritoneBoulevard),
            LocationButton(Location.TenorTerrace),

        ],
        Location.AltoAvenue: [
            LocationButton(Location.LoopyLane),
            LocationButton(Location.MinniesMelodyland),
        ],
        Location.TenorTerrace: [
            LocationButton(Location.LullabyLane),
            LocationButton(Location.MinniesMelodyland),
        ],
        Location.BaritoneBoulevard: [
            LocationButton(Location.SleetStreet),
            LocationButton(Location.MinniesMelodyland),
        ],

        Location.TheBrrrgh: [
            LocationButton(Location.WalrusWay),
            LocationButton(Location.PolarPlace),
            LocationButton(Location.SleetStreet),
        ],
        Location.WalrusWay: [
            LocationButton(Location.LighthouseLane),
            LocationButton(Location.TheBrrrgh),
        ],
        Location.PolarPlace: [
            # LBHQ
            LocationButton(Location.TheBrrrgh),
        ],
        Location.SleetStreet: [
            LocationButton(Location.BaritoneBoulevard),
            LocationButton(Location.TheBrrrgh),
        ],
        Location.DonaldsDreamland: [
            LocationButton(Location.PajamaPlace),
            LocationButton(Location.LullabyLane),
        ],
        Location.PajamaPlace: [
            # CBHQ
            LocationButton(Location.DonaldsDreamland),
        ],
        Location.LullabyLane: [
            LocationButton(Location.TenorTerrace),
            LocationButton(Location.DonaldsDreamland),
        ],
        Location.MyEstate: [
            LocationButton(Location.ToontownCentral),
        ],
    }

    def __init__(self, user: discord.User):
        """
        :param user: user reserved for this interaction
        """
        super().__init__()
        self.user = user.id

        # our initial call to init and communicate with the database
        db = DatabaseManager

        # Check to see if user is registered in database
        user_db = (db.session.query(db.User).filter_by(disid=self.user).first())
        if not user_db:
            # register the new user
            user = db.User(self.user, str(user))
            self.context = user.registerFishContext(FishContext())  # returns FishContext
            db.session.add(user)
            db.session.commit()
            # todo, move these to a check to see if user is new to campaign
            # since they are a new user, let's apply some default values:
            self.context.JELLYBEANS_TOTAL = 20  # to start them off, give them 20 jellybeans.
            # or maybe we can just give them a grace cast ^
            self.context.BUCKET_SIZE_MAX = 20  # default bucket size
            self.context.ROD_ID = FishingRod.TWIG_ROD  # beginner rod
        else:
            # nope, he's already registered with us, register the pre-existing context blob.
            self.context = user_db.context

        # set our db marker if haven't already, this is done upon the first command executed in the bot session
        FishInternal.db = db

        # for convenience of db updates, we give the context object a pointer to the userid.
        self.context.disid = self.user

        # let's ensure that session-based values are their default values:
        self.context.CAUGHT_FISH_SESSION = 0

        # also, ensure some default values exist for us.
        self.adjust_context_entries()

        # since we've modified context, might as well register the disid value into the context blob
        db.updateContext(self.user, self.context)

        # now that everything's ready to go, we can show the user their next options.
        self.main_menu()

    def adjust_context_entries(self):
        """
        if a user ends up crashing because of a missing attribute, this is a safety function
        """
        if not hasattr(self.context, "JELLYBEANS_TOTAL"):
            self.context.JELLYBEANS_TOTAL = 0

        if not hasattr(self.context, "ROD_ID"):
            self.context.ROD_ID = FishingRod.TWIG_ROD

        if not hasattr(self.context, "BUCKET_SIZE_MAX"):
            self.context.BUCKET_SIZE_MAX = 20

        if not hasattr(self.context, "FISH_DATA"):
            self.context.FISH_DATA = dict()


    def disable_buttons(self):
        for button in self.children:
            button.disabled = True

    def is_host(self, user):
        return self.user == user

    def main_menu(self):
        # self.add_item(MainMenuButton(GameMode.CAMPAIGN, label = "Campaign"))
        self.add_item(MainMenuButton(GameMode.FREE_PLAY, label = "Free Play"))

    def location_options(self, location):
        """
        given an area, display possible paths using LocationButtons dict.
        """
        # Add fishing button first.
        if location != Location.NONE:
            self.add_item(FishHereButton())

        places = self.LocationButtons.get(location)
        for place in places:
            self.add_item(place)

    def campaign_options(self, campaign_context):
        tutorial = True
        if tutorial:
            pass
        pass

    def fish_options(self):
        self.add_item(FishButton(full=self.context.BUCKET_FULL, poor=self.context.JELLYBEANS_TOTAL <= 0))
        # check to see if our state changed to talk to the fisherman instead
        # if state changed, don't show fisherman button
        self.add_item(VisitFishermanButton(label = "See Fisherman"))

        # temp back button
        self.add_item(LocationButton(self.context.LOCATION_ID, label="Go Back"))

    def fisherman_options(self):
        # only here to prevent a softlock, needs to be a back button instead
        self.add_item(FishHereButton())
        # self.add_item(FishingRodDropdown())
        self.add_item(SellButton(disabled=self.context.BUCKET_SIZE == 0))
        # todo: disable go shopping in free play
        # self.add_item(ShopButton(label = "Go Shopping"))
        # check stats, inventory to change equipped rod
        self.add_item(InventoryButton(label = "Access Inventory"))

    def inventory_options(self):
        # temp until we have a back button
        self.add_item(VisitFishermanButton(label = "Back to Fisherman"))
        self.add_item(FishingRodDropdown())
        self.add_item(ViewRecordsButton())

    def shop_options(self):
        self.add_item(VisitFishermanButton(label = "See Fisherman"))
        self.add_item(UpgradeButton(label = "Upgrade Fishing Rod"))


    # @discord.ui.button(label='Check Fishing Statistics', style=discord.ButtonStyle.secondary, )
    # async def button_stats(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     context.GAME_MODE = GameMode.FREE_PLAY
    #     em = discord.Embed(
    #         title = "ToonTask",
    #         description = str(f"gm = {context.GAME_MODE} - intended {GameMode.CAMPAIGN}"),
    #     )
    #     await interaction.response.edit_message(embed = em)
    #     self.disable = False
    #
    #     self.stop()
    #
    #
    # @discord.ui.button(label='Simulate Fishing', style=discord.ButtonStyle.secondary)
    # async def button_autosim(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     context.GAME_MODE = GameMode.FREE_PLAY
    #     em = discord.Embed(
    #         title = "ToonTask",
    #         description = str(f"gm = {context.GAME_MODE} - intended {GameMode.CAMPAIGN}"),
    #     )
    #     await interaction.response.edit_message(embed = em)
    #     self.stop()


@bot.tree.command()
async def gofish(interaction: discord.Interaction):
    files = [
        discord.File("img/game_logo_1.png", filename = "game_logo_1.png"),
        discord.File("img/game_bg.png", filename = "game_bg.png")
    ]

    em = discord.Embed(
        title = "Gone Fishin'!",
        description = f"[Github Repository](https://github.com/loonaticx/fishing-game)",
        color = discord.Color.from_str("#49F147"),
    )
    em.set_thumbnail(url = "attachment://game_logo_1.png")
    em.set_image(url = "attachment://game_bg.png")
    em.add_field(name = "Bot Version", value = f"v.0.8")
    # em.add_field(name = "Github Repository", value = f"https://github.com/loonaticx/fishing-game")

    adjective = (
        "succulent",
        "zesty",
        "wacky",
        "scrumptious",
        "one and only"

    )
    em.set_footer(text=f"Discord bot created by the {random.choice(adjective)} loonatic#1337")

    view = MasterView(user = interaction.user)
    await interaction.response.send_message(embed = em, view = view, files = files)


async def rods_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    options = rodEnums
    # for entry in options:
    #     print(entry)
    return [
        app_commands.Choice(name = str(entry), value = str(entry))
        for entry in options
    ]


class CastGroup(app_commands.Group):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot
        self.name = "cast"

    @app_commands.command(name = "hyper")
    async def hypercast(self, interaction: discord.Interaction,
                        rod_id: FishingRod = FishingRod.GOLD_ROD,
                        num_iter: int = 1000):
        num_iter = abs(num_iter)
        if num_iter > 50000:
            await interaction.response.send_message(
                content = "Sorry, I don't want to process that many iterations. (max 50000)", ephemeral = True
            )
            return
        sim = FishSim.testRarity(rod_id, num_iter)
        desc = f"Generated rarity report for {num_iter} casts:\n"
        for entry in sim.keys():
            desc += f"{entry}: {sim[entry]:.2f}%\n"
        await interaction.response.send_message(content = desc)

    @app_commands.command(name = "mega")
    async def megacast(self, interaction: discord.Interaction, num_casts: int = 1, hit_rate: float = 0.8):
        num_casts = abs(num_casts)
        hit_rate = abs(hit_rate)
        desc = ""
        if hit_rate > 1:
            await interaction.response.send_message(content = "hit rate must be between 0 and 1", ephemeral = True)
            return
        if num_casts > 1:
            await interaction.response.send_message(
                content = "Sorry, I don't want to process that many iterations. (max 1)", ephemeral = True
            )
            return
        pondData, rodData = FishSim.generateFishingReport(num_casts, hit_rate)
        for entry in rodData:
            desc += f"{entry}\n"
        # desc = f"pond data\n{pondData}\n\nrod data\n{rodData}"
        # desc = f"Generated rarity report for {num_iter} casts:\n"
        # for entry in sim.keys():
        #     desc += f"{entry}: {sim[entry]:.2f}%\n"
        await interaction.response.send_message(content = desc)


class DatabaseGroup(app_commands.Group):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot
        self.name = "database"

    @app_commands.command(name = "lookup")
    async def database_lookup(self, interaction: discord.Interaction, user: discord.User):
        user_id = user.id
        if user_id != config.OWNER_USER:
            await interaction.response.send_message(f"go away u dont have access to this command")
            return
        username = user.name
        avatar = user.display_avatar.url
        db = DatabaseManager
        # Originally, implementation of context was done on bot init. meaning everyones progress was shared
        # to ensure users arent interfering with other peoples game, we must create our own context.

        # Check to see if user has already been registered in database
        user_db = (db.session.query(db.User).filter_by(disid = user_id).first())
        if not user_db:
            await interaction.response.send_message(f"user {username} is not registered in db")
            return

        context = user_db.context

        def getFields(context):
            attrs = {
                "entries": {},
                "null": []
            }
            for name in dir(context):
                if name.startswith("_"):
                    continue
                if not hasattr(context, name):
                    # user doesnt have a value yet for such attribute
                    attrs["null"].append(name)
                    continue
                attr = getattr(context, name)
                # if callable(attr):
                #     continue
                attrs["entries"][name] = attr
            return attrs

        pretty_string = ""
        fields = getFields(context)
        for field in fields.keys():
            pretty_string += f"**{field}**: ```python\n{fields[field]}```\n"

        pretty_string_user = ""
        fields_user = getFields(user_db)
        for field in fields_user.keys():
            pretty_string_user += f"**{field}**: {(entry for entry in field)}\n"

        em = discord.Embed(
            title = f"db info for {username}",
            description = f"__FishContext__\n{pretty_string}\n__User__\n{pretty_string_user}",
            color = discord.Color.from_str("#49F147"),
        )
        await interaction.response.send_message(embed = em)

if ALL_SERVERS:
    bot.tree.add_command(DatabaseGroup(bot))
    bot.tree.add_command(CastGroup(bot))
else:
    bot.tree.add_command(DatabaseGroup(bot), guild = MY_GUILD)
    bot.tree.add_command(CastGroup(bot), guild = MY_GUILD)


bot.run(config.BOT_TOKEN)
