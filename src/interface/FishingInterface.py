"""
main interface seen when fishing
"""
import random

from rich import print
from rich.box import Box
from rich.console import Group, Console
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
import time
from rich.progress import track
from rich.table import Table


class FishingInterface():
    def __init__(self):
        self.buildInterface()
        self.testEntry = [
            ['a', 'a', 'a', 'a'],
            ['b', 'b', 'b', 'b'],
            ['c', 'c', 'c', 'c'],
            ['d', 'd', 'd', 'd'],
        ]


    def buildInterface(self):
        # currentStats = Panel("test", height = 3)
        # amt of fish in bucket
        # amt of jellybeans in jar
        self.console = Console()
        self.catchTable = Table()
        self.catchTable.add_column("Fish #")
        self.catchTable.add_column("Fish Name")
        self.catchTable.add_column("Weight")
        self.catchTable.add_column("Jellybeans")

        catchFeedPanel = Panel.fit(title="[yellow]Fishing Bucket[/yellow]", renderable =self.catchTable)

        self.layout = Layout()
        self.layout.split_column(
            # Layout(currentStats),
            Layout(name = "lower")
        )
        self.layout["lower"].split_row(
            Layout(name = "left"),
            Layout(catchFeedPanel),
        )
        # self.layout["right"] = self.catchTable
        # self.layout[self.catchTable].update(self.catchTable)

        # panelB = Panel('testb', style = "on red")
        #
        # group = Group(
        #     panelA,
        #     panelB
        # )
        # print(Panel(group))

    def enterInterface(self):
        console.clear()
        console.print(self.layout)
        f.goFish()

    def goFish(self):
        ans = self.promptFish()
        if ans == 'fish':
            for _ in track(range(3), description = "Fishin'..."):
                time.sleep(1)  # Simulate work being done
            # generate fish results
            self.addFish(self.testEntry[random.randint(0, 3)])
            # console.clear()
            # self.layout["lower"].update(self.catchTable)
            with Live(self.layout, refresh_per_second = 1) as live:
                # time.sleep(1)
                console.clear()
                self.layout["lower"].update(self.catchTable)
            self.goFish()

        # self.catchTable.add_row(
        #     f"{self.ids[i]}", f"{self.names[i]}", f"{self.weight[i]}", f"{self.cost[i]}"
        # )
        # ret fish results

    def updateTable(self, table, i):
        # THIS WORKS but prints out a new table each time
        with Live(table, refresh_per_second = 4) as live:  # update 4 times a second to feel fluid
            table.add_row(f"{self.ids[i]}", f"{self.names[i]}", f"{self.weight[i]}", f"{self.cost[i]}")
            # self.layout["lower"].update(self.catchTable)

    def addFish(self, caughtFish):
        id = caughtFish[0]
        name = caughtFish[1]
        weight = caughtFish[2]
        cost = caughtFish[3]
        self.catchTable.add_row(
            id, name, weight, cost
        )
        return self.catchTable

    def updateCatchTable(self) -> Table:
        # THIS eh
        catchTable = Table()
        catchTable.add_column("Fish #")
        catchTable.add_column("Fish Name")
        catchTable.add_column("Weight")
        catchTable.add_column("Jellybeans")
        for i in range(len(self.ids)):
            catchTable.add_row(
                f"{self.ids[i]}", f"{self.names[i]}", f"{self.weight[i]}", f"{self.cost[i]}"
            )
        return catchTable

    def test(self, t):
        self.ids = [1, 2, 3]
        self.names = ['fish'] * 3
        self.weight = [3] * 3
        self.cost = [3] * 3

        with Live(self.layout, refresh_per_second = 1) as live:
            for i in range(len(t)):
                time.sleep(1)
                self.layout["lower"].update(self.addFish(t[i]))
                # self.layout["lower"].update(self.catchTable)

    def promptFish(self):
        self.questions = [
            {
                "type": "list",
                "name": 'response',
                "choices": ['fish', 'goto fisherman'],
                "message": 'what do u wanna do',
                'filter': lambda val: val.lower().split(None)[0]
            }
        ]
        return prompt(self.questions).get('response')

        pass

if __name__ == "__main__":
    from fishbase.FishBase import FishBase

    base = FishBase()
    f = FishingInterface()
    f.buildInterface()


    test = [
        ['a', 'a', 'a', 'a'],
        ['b', 'b', 'b', 'b'],
        ['c', 'c', 'c', 'c'],
        ['d', 'd', 'd', 'd'],
    ]

    f.enterInterface()

    # f.test(test)
    # f.promptFish()
    # f.updateLayout()
