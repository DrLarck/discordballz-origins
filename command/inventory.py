"""
Inventory command

--

Author : DrLarck

Last update : 07/09/20 by DrLarck
"""

from discord.ext import commands

# util
from utility.entity.player import Player
from utility.command.checker import CommandChecker

# tool
from utility.command.tool.tool_inventory import ToolInventory


class CommandInventory(commands.Cog):

    def __init__(self, client):
        self.client = client

        # Private
        self.__tool = ToolInventory(self.client)

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.command(aliases=["inv"])
    async def inventory(self, context):
        # Log
        await self.client.logger.log(context)

        # Init
        player = Player(context, self.client, context.message.author)
        inventory = await self.__tool.get_inventory_embed(player)

        await context.send(embed=inventory)


def setup(client):
    client.add_cog(CommandInventory(client))
