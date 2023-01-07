from typing import Optional, List

import discord
from discord import app_commands
from discord.ext import commands

from fishbase import RodInfo
from fishbase.FishContext import FishContext
from fishbase.FishContext import FishInternal

import DatabaseManager
# from fishbase.EnumBase import *
from fishbase.FishGameGlobals import getFishDict
from fishbase.RodInfo import *
import random
from config import config
from testing import fishaccess as FishSim

MY_GUILD = discord.Object(id = config.BOT_GUILD)  # replace with your guild id


class FishingSimBot(commands.Bot):

    def __init__(self, intents, command_prefix, description):
        super().__init__(intents = intents, command_prefix = command_prefix, description = description)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
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
        em.add_field(name="Total Jellybeans",value=view.context.JELLYBEANS_TOTAL)
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

        # if i wanted to be ambitious i could take pictures of areas n set them as images

        em = discord.Embed(
            title = "Ready to fish!",
            description = str(f"uhh probably a list of all the first that can be caught here"),
        )

        em.add_field(name = "Fishing Bucket", value = f"{4}/20")
        em.add_field(name = "Total Jellybeans", value = f"{view.context.JELLYBEANS_TOTAL}")
        em.add_field(name = "Fish Bingo?", value = f"No")

        em.set_footer(text = f"Selected Rod: {FishingRodNameDict[view.context.ROD_ID]} | Current Location: {view.context.LOCATION_ID}")

        randomfish = f"fish_{random.randint(1, 5)}.png"
        thumbnail = discord.File(f"img/{randomfish}", filename = randomfish)
        em.set_thumbnail(url = f"attachment://{randomfish}")

        view.fish_options()
        await interaction.response.edit_message(embed = em, view = view, attachments = [thumbnail])


class FishButton(discord.ui.Button['MasterView']):
    def __init__(self, label = "Cast", style = discord.ButtonStyle.red):
        super().__init__(style = style, label = label)

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
        view.context.CAUGHT_FISH_SESSION += 1
        caughtFish = FishSim.FishSpeciesNames[genus][species]
        fishValue = FishSim.getValue(genus, species, weight)

        profit = fishValue - RodInfo.rodDict[view.context.ROD_ID][2]
        view.context.JELLYBEANS_TOTAL += profit  # Lazy shortcut so that we dont need to call the db twice for casting

        rarity = FishSim.fishdict[genus][species][2]
        if rarity in range(1, 3):
            # common
            rarity_desc = "Common"
            color = "#6FE258"
        elif rarity in range(3, 6):
            # uncommon
            rarity_desc = "Uncommon"
            color = "#58AAE2"
        elif rarity in range(6, 8):
            # rare
            rarity_desc = "Rare"
            color = "#EC3A31"
        elif rarity in range(8, 10):
            # ultra rare
            rarity_desc = "Ultra Rare"
            color = "#EBF425"
        else:
            # unknown
            rarity_desc = ""
            color = "#9C9C9C"

        # if new species
        if False:
            color = "#338DFF"

        border = discord.Color.from_str(color)

        new = "\n**NEW SPECIES!**"
        record = "\n**NEW RECORD!**"

        image = discord.File(f"img/tt_fish_{genus}.gif", filename = f"tt_fish_{genus}.gif")


        em = discord.Embed(
            title = f"Caught: {caughtFish}",
            description = str(f"{new}"),
            color = border
        )
        em.add_field(name = "Rarity", value = f"{rarity}/10 ({rarity_desc})")
        em.add_field(name = "Weight", value = f"{weight} oz (Highest: 5.8 oz)")

        em.add_field(name = "Fishing Bucket", value = f"{4}/20")
        em.add_field(name = "Jellybean Amount", value = f"{fishValue}")
        em.add_field(name = "Total Jellybeans", value = f"{view.context.JELLYBEANS_TOTAL} ({profit})")  # + or - if profit


        em.set_footer(text = f"Selected Rod: {FishingRodNameDict[view.context.ROD_ID]} | Current Location: {view.context.LOCATION_ID}"
                             f" | Fish Caught in Session: {view.context.CAUGHT_FISH_SESSION}")
        em.set_image(url = f"attachment://tt_fish_{genus}.gif")

        randomfish = f"fish_{random.randint(1, 5)}.png"
        thumbnail = discord.File(f"img/{randomfish}", filename = randomfish)
        em.set_thumbnail(url = f"attachment://{randomfish}")

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
        image = discord.File(f"img/npc_freddy.png", filename = f"npc_freddy.png")

        em = discord.Embed(
            title = "FISHERMAN FREDDY",
            description = str(f"no way im fisherman freddy"),
        )
        # can colorize these based off rarity
        report = "Clown Fish\nPuppy Dog Fish\nPool Shark\nPeanut Butter & Jellyfish\nNurse Shark\nHoley Mackerel\nDevil Ray"
        em.add_field(name="Fishing Bucket",value=report)
        em.set_thumbnail(url="attachment://npc_freddy.png")
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

        em = discord.Embed(
            title = "Fishing Shop",
            description = "what the heck is on sale today",
        )
        view.shop_options()
        # remove empty attachment list later
        await interaction.response.edit_message(embed = em, view = view, attachments = [])


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
    # maybe location buttons can light up green if theyve caught all the possible fish for that area
    def __init__(self, location: Location, label, style = discord.ButtonStyle.blurple):
        super().__init__(style = style, label = label)
        self.location = location

    async def callback(self, interaction: discord.Interaction):
        # the function that edits the message
        assert self.view is not None
        view: MasterView = self.view
        if not view.is_host(interaction.user.id):
            await interaction.response.send_message("Sorry, this is not your game.", ephemeral = True)
            return

        view.context.LOCATION_ID = self.location
        view.clear_items()
        # Notes: we can do if location in (playgrounds), then go into an if chain? :X
        files = []

        # We're arriving to a playground
        if view.context.LOCATION_ID == Location.ToontownCentral:
            # can include all possible fish you can catch here
            em = discord.Embed(
                title = "toontown central",
                description = str(f"THIS IS THE TOONTWON CENTRAL PLAYGROUND list stretes here or something"),
            )
        else:
            em = discord.Embed(
                title = "stupid playground",
                description = str(f"gm = {view.context.GAME_MODE} - intended {GameMode.CAMPAIGN}"),
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


        view.inventory_options()
        # Re-load the inventory view to show our changes.
        await interaction.response.edit_message(view=view, embed=em)


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
        em.add_field(name="Rod Price", value=RodPriceDict[view.context.ROD_ID])

        rodinfo = rodDict[view.context.ROD_ID]
        em.add_field(name="Fish Weight", value=f"Min: {rodinfo[0]}, Max: {rodinfo[1]}")
        em.add_field(name="Rod Cast Cost", value=rodinfo[2])
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
            LocationButton(Location.ToontownCentral, label = "Toontown Central"),
            LocationButton(Location.DonaldsDock, label = "Donalds Dock")
        ],
        Location.ToontownCentral: [
            LocationButton(Location.PunchlinePlace, label = "Punchline Place"),
            LocationButton(Location.LoopyLane, label = "Loopy Lane"),
            LocationButton(Location.SillyStreet, label = "Silly Street"),
        ],
        Location.PunchlinePlace: [
            LocationButton(Location.ToontownCentral, label = "Toontown Central"),
            LocationButton(Location.DonaldsDock, label = "Donalds Dock"),
        ],
        Location.SillyStreet: [
            LocationButton(Location.ToontownCentral, label = "Toontown Central"),
        ],
        Location.LoopyLane: [
            LocationButton(Location.ToontownCentral, label = "Toontown Central"),
        ],
        Location.DonaldsDock: [
            LocationButton(Location.PunchlinePlace, label = "Punchline Place"),
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
            self.context.BUCKET_SIZE = 20  # default bucket size
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
        if not hasattr(self.context, "JELLYBEANS_TOTAL"):
            self.context.JELLYBEANS_TOTAL = 20

        # since we've modified context, might as well register the disid value into the context blob
        db.updateContext(self.user, self.context)

        # now that everything's ready to go, we can show the user their next options.
        self.main_menu()

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
        self.add_item(FishButton())
        # check to see if our state changed to talk to the fisherman instead
        # if state changed, don't show fisherman button
        self.add_item(VisitFishermanButton(label = "See Fisherman"))

        # temp back button
        self.add_item(LocationButton(self.context.LOCATION_ID, label="Go Back"))

    def fisherman_options(self):
        # only here to prevent a softlock, needs to be a back button instead
        self.add_item(FishButton())
        # self.add_item(FishingRodDropdown())

        # todo: disable go shopping in free play
        # self.add_item(ShopButton(label = "Go Shopping"))
        # check stats, inventory to change equipped rod
        self.add_item(InventoryButton(label = "Access Inventory"))

    def inventory_options(self):
        # temp until we have a back button
        self.add_item(VisitFishermanButton(label = "Back to Fisherman"))
        self.add_item(FishingRodDropdown())

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
        discord.File("img/game_logo_2.png", filename = "game_logo_2.png"),
        discord.File("img/game_bg.png", filename = "game_bg.png")
    ]

    em = discord.Embed(
        title = "Gone Fishin'!",
        description = f"[Github Repository](https://github.com/loonaticx/fishing-game)",
        color = discord.Color.from_str("#49F147"),
    )
    em.set_thumbnail(url = "attachment://game_logo_2.png")
    em.set_image(url = "attachment://game_bg.png")
    em.add_field(name = "Bot Version", value = f"v.0.7")
    em.add_field(name = "Github Repository", value = f"https://github.com/loonaticx/fishing-game")

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
    for entry in options:
        print(entry)
    return [
        app_commands.Choice(name = str(entry), value = str(entry))
        for entry in options
    ]

@bot.tree.command()
# idk why this isnt working rn:
# @app_commands.autocomplete(
#     rod_id = rods_autocomplete
# )
async def hypercast(interaction: discord.Interaction, rod_id:FishingRod, num_iter:int):
    num_iter = abs(num_iter)
    if num_iter > 50000:
        await interaction.response.send_message(content = "Sorry, I don't want to process that many iterations. (max 50000)", ephemeral=True)
        return
    sim = FishSim.testRarity(rod_id, num_iter)
    desc = f"Generated rarity report for {num_iter} casts:\n"
    for entry in sim.keys():
        desc += f"{entry}: {sim[entry]:.2f}%\n"
    await interaction.response.send_message(content = desc)

@bot.command()
async def megacast(ctx:commands.Context, num_casts: int = 1, hit_rate:float=0.8):
    num_casts = abs(num_casts)
    hit_rate = abs(hit_rate)
    desc = ""
    if hit_rate > 1:
        await ctx.send( "hit rate must be between 0 and 1")
        return
    if num_casts > 1:
        await ctx.send("Sorry, I don't want to process that many iterations. (max 1)")
        return
    pondData, rodData = FishSim.generateFishingReport(num_casts, hit_rate)
    for entry in rodData:
        desc += f"{entry}\n"
    # desc = f"pond data\n{pondData}\n\nrod data\n{rodData}"
    # desc = f"Generated rarity report for {num_iter} casts:\n"
    # for entry in sim.keys():
    #     desc += f"{entry}: {sim[entry]:.2f}%\n"
    await ctx.send(desc)



@bot.tree.command()
async def dblookup(interaction: discord.Interaction, user: discord.User):
    user_id = user.id
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
        pretty_string += f"**{field}**: {fields[field]}\n"

    pretty_string_user = ""
    fields_user = getFields(user_db)
    for field in fields_user.keys():
        pretty_string_user += f"**{field}**: {(entry for entry in field)}\n"


    em = discord.Embed(
        title = f"db info for {username}",
        description = f"__FishContext__\n{pretty_string}\n__User__\n{pretty_string_user}",
        color = discord.Color.from_str("#49F147"),
    )
    await interaction.response.send_message(embed=em)


bot.run(config.BOT_TOKEN)
