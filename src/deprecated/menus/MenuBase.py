"""
Base class used by all the menus. Does a lot of the configuration
"""

from rich.table import Table
from rich.panel import Panel
from enum import IntEnum
from rich import print
from rich.console import Console
from rich.prompt import Prompt


class MenuBase:

    def __init__(self):
        self.title = "Menu Base"  # Header of the menu table
        self.prompt = "Where would you like to go?"
        self.response = "response"
        self.menuOption = dict()  # Ex: MainMenuOptions in FishGameGlobals
        self.items = []  # [ (Item Name, Item Info) ]
        self.result: IntEnum  # Value from menuOption

        # for future
        self.menu: Panel
        self.stages = [0] * 1  # length = number of stages, at least one entry
        self.currentStage = self.stages[0]

        # customize table menu
        self.tableHeader_visible = False
        self.tableHeader_style = "bold_magenta"
        self.columnStyle = "dim"

        self.questions = [
            {
                "type": "list",
                "name": self.response,
                "choices": list(),
                "message": self.prompt,
                'filter': lambda val: val.lower().split(None)[0]
            }
        ]

    def enterMenu(self, printHeader=False, headerText=""):
        console.clear()
        if headerText:
            printHeader = True
        if printHeader:
            console.print(headerText)
        self.result = self.buildMenu()
        self.parseResult(self.result[self.response])

    def buildMenu(self):
        MenuTable = Table(show_header = self.tableHeader_visible, header_style = self.tableHeader_style)
        MenuTable.add_column(self.title, style = self.columnStyle)
        index = 1
        options = []
        for item in self.items:
            (title, desc, *ext) = item
            MenuTable.add_row(str(index), title, desc)
            index += 1
            options.append(title)

        self.questions[0]['choices'] = options

        console.print(MenuTable)
        return prompt(self.questions)

    def parseResult(self, resultIn, stage=0):
        """
        :param str resultIn: Input value
        :param int stage: Stage level
        """
        self.result = self.menuOption.get(resultIn)
        # self.result = GameMode(resultIn)
