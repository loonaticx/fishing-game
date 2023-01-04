from typing import Optional, List

import discord
from discord import app_commands
from discord.ext import commands
from fishbase.FishContext import FishContext

context = FishContext()

from fishbase.EnumBase import *
import random
from config import config

MY_GUILD = discord.Object(id = config.BOT_GUILD)  # replace with your guild id


class MyBot(commands.Bot):
    # context = FishContext()

    def __init__(self, intents, command_prefix, description):
        super().__init__(intents=intents, command_prefix=command_prefix, description = description)
        # __builtins__['context'] = self.context


    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild = MY_GUILD)
        await self.tree.sync(guild = MY_GUILD)


intents = discord.Intents.default()
intents.message_content = True  # required for dropdown

bot = MyBot(command_prefix = '/', description = 'blah', intents = intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.competing, name = "fish gaming"))


class MainMenuButton(discord.ui.Button['MasterView']):
    def __init__(self, game_mode: GameMode, label, style=discord.ButtonStyle.secondary):
        super().__init__(style=style, label=label)
        self.mode = game_mode

    async def callback(self, interaction: discord.Interaction):
        # the function that edits the message
        assert self.view is not None
        view: MasterView = self.view
        context.GAME_MODE = self.mode
        view.clear_items()

        if context.GAME_MODE == GameMode.CAMPAIGN:
            em = discord.Embed(
                title = "Select Starting Playground",
                description = str(f"gm = {context.GAME_MODE} - intended {GameMode.CAMPAIGN}"),
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
                description = str(f"gm = {context.GAME_MODE} - intended {GameMode.CAMPAIGN}"),
            )
            view.location_options(Location.TOONTOWN_CENTRAL)

        await interaction.response.edit_message(embed = em, view=view)


class FishHereButton(discord.ui.Button['MasterView']):
    # this is here ONLY TO ENTER THE FISHING MENU
    def __init__(self,  label="Go Fishing!", style=discord.ButtonStyle.red):
        super().__init__(style=style, label=label)

    async def callback(self, interaction: discord.Interaction):
        # the function that edits the message
        assert self.view is not None
        view: MasterView = self.view
        view.clear_items()

        thumbnail = discord.File("img/fish_1.png", filename = "fish_1.png")
        # if i wanted to be ambitious i could take pictures of areas n set them as images

        em = discord.Embed(
            title = "Ready to fish!",
            description = str(f"uhh probably a list of all the first that can be caught here"),
        )

        em.add_field(name="Fishing Bucket", value = f"{4}/20")
        em.add_field(name="Total Jellybeans", value = f"{69}")
        em.add_field(name="Fish Bingo?", value = f"No")

        em.set_footer(text = f"Selected Rod: Blah | Current Location: Silly Street")
        em.set_thumbnail(url = "attachment://fish_1.png")
        view.fish_options()
        await interaction.response.edit_message(embed = em, view=view, attachments = [thumbnail])


class FishButton(discord.ui.Button['MasterView']):
    def __init__(self, label="Cast", style=discord.ButtonStyle.red):
        super().__init__(style=style, label=label)

    async def callback(self, interaction: discord.Interaction):
        # do our initial housekeeping:
        assert self.view is not None
        view: MasterView = self.view
        view.clear_items()
        # ok, user has pressed the button. let's do some calculations.

        file = discord.File("img/clownfish.gif", filename = "clownfish.gif")
        file2 = discord.File("img/fish_1.png", filename = "fish_1.png")

        new = "\n**NEW SPECIES!**"
        record = "\n**NEW RECORD!**"
        border = discord.Color.from_str("#338DFF")  # if new species
        em = discord.Embed(
            title = "Caught: Circus Clown Fish",
            description = str(f"{new}"),
            color=border
        )
        em.add_field(name="Rarity", value = f"13.03% (Rare)")
        em.add_field(name="Weight", value = f"5.4 oz (Highest: 5.8 oz)")

        em.add_field(name="Fishing Bucket", value = f"{4}/20")
        em.add_field(name="Jellybean Amount", value = f"{12}")
        em.add_field(name="Total Jellybeans", value = f"{69}")

        em.set_footer(text = f"Selected Rod: Blah | Current Location: Silly Street")
        em.set_image(url = "attachment://clownfish.gif")
        em.set_thumbnail(url = "attachment://fish_1.png")

        view.fish_options()
        await interaction.response.edit_message( attachments=[file, file2], embed = em, view=view)


class VisitFishermanButton(discord.ui.Button['MasterView']):
    def __init__(self, label, style=discord.ButtonStyle.green):
        super().__init__(style=style, label=label)

    async def callback(self, interaction: discord.Interaction):
        # the function that edits the message
        assert self.view is not None
        view: MasterView = self.view
        view.clear_items()

        em = discord.Embed(
            title = "FISHERMAN FREDDY",
            description = str(f"no way im fisherman freddy"),
        )
        view.fish_options()
        # remove empty attachment list later
        await interaction.response.edit_message(embed = em, view=view, attachments=[])

class BackButton(discord.ui.Button['MasterView']):
    def __init__(self, label="Go Back", style=discord.ButtonStyle.gray):
        super().__init__(style=style, label=label)

    async def callback(self, interaction: discord.Interaction):
        # the function that edits the message
        assert self.view is not None
        view: MasterView = self.view
        view.clear_items()
        # ok, first thing we need to do is see what we're doing:
        # check to see if we've selected a game mode.

        # are we currently selling fish? return to main fish panel

        # are we currently in main fish panel? return to last location

        # if location id is none, what do?
        view.location_options(context.LOCATION_ID)
        await interaction.response.edit_message(embed = None, view=view)


class LocationButton(discord.ui.Button['MasterView']):
    # maybe location buttons can light up green if theyve caught all the possible fish for that area
    def __init__(self, location: Location, label, style=discord.ButtonStyle.blurple):
        super().__init__(style=style, label=label)
        self.location = location

    async def callback(self, interaction: discord.Interaction):
        # the function that edits the message
        assert self.view is not None
        view: MasterView = self.view
        context.LOCATION_ID = self.location
        view.clear_items()
        # Notes: we can do if location in (playgrounds), then go into an if chain.

        # We're arriving to a playground
        if context.LOCATION_ID == Location.TOONTOWN_CENTRAL:
            # can include all possible fish you can catch here
            em = discord.Embed(
                title = "toontown central",
                description = str(f"THIS IS THE TOONTWON CENTRAL PLAYGROUND list stretes here or something"),
            )
        else:
            em = discord.Embed(
                title = "stupid playground",
                description = str(f"gm = {context.GAME_MODE} - intended {GameMode.CAMPAIGN}"),
            )

        view.location_options(context.LOCATION_ID)
        await interaction.response.edit_message(embed = em, view=view)


class MasterView(discord.ui.View):
    LocationButtons = {
        # maybe if player completes all fish for a certain street, they can visit that street from another
        # ex: loopy --> punchline
        # this would require us to change from lists to sets
        Location.NONE: [
            LocationButton(Location.TOONTOWN_CENTRAL, label = "Toontown Central"),
            LocationButton(Location.DonaldsDock, label = "Donalds Dock")
        ],
        Location.TOONTOWN_CENTRAL: [
            LocationButton(Location.PUNCHLINE_PLACE, label = "Punchline Place"),
            LocationButton(Location.LoopyLane, label = "Loopy Lane"),
            LocationButton(Location.SillyStreet, label = "Silly Street"),
        ],
        Location.PUNCHLINE_PLACE: [
            LocationButton(Location.TOONTOWN_CENTRAL, label = "Toontown Central"),
            LocationButton(Location.DonaldsDock, label = "Donalds Dock"),
        ],
        Location.SillyStreet: [
            LocationButton(Location.TOONTOWN_CENTRAL, label = "Toontown Central"),
        ],
        Location.LoopyLane: [
            LocationButton(Location.TOONTOWN_CENTRAL, label = "Toontown Central"),
        ],
        Location.DonaldsDock: [
            LocationButton(Location.PUNCHLINE_PLACE, label = "Punchline Place"),
        ],
    }

    def __init__(self):
        super().__init__()
        self.main_menu()

    def disable_buttons(self):
        for button in self.children:
            button.disabled = True

    def main_menu(self):
        self.add_item(MainMenuButton(GameMode.CAMPAIGN, label="Campaign"))
        self.add_item(MainMenuButton(GameMode.FREE_PLAY, label="Free Play"))

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

    def fish_options(self):
        self.add_item(FishButton())
        # check to see if our state changed to talk to the fisherman instead
        # if state changed, don't show fisherman button
        self.add_item(VisitFishermanButton(label = "See Fisherman"))


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
async def ftest(interaction: discord.Interaction):
    em = discord.Embed(
        title = "ToonTask",
        description = str(f"emtest"),
    )
    view = MasterView()
    await interaction.response.send_message(embed=em, view=view)



bot.run(config.BOT_TOKEN)
