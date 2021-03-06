"""Character tool for the player like lock/unlock and info displaying

@author DrLarck

@update 29/01/21 by DrLarck"""

from discord.ext import commands

# util
from utility.entity.player import Player
from utility.command.checker import CommandChecker
from utility.command.tool.tool_help import ToolHelp
from utility.entity.character import CharacterGetter
from utility.global_tool import GlobalTool
from utility.graphic.icon import GameIcon


class CommandCharacter(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.icon = GameIcon()
        self.tool = GlobalTool()
        self.rarity = ['n', 'r', "sr", "ssr", "ur", "lr"]
    
    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.group(invoke_without_command=True, aliases=["char"])
    async def character(self, context):
        """Display the character help"""

        player = Player(context, self.client, context.message.author)
        help = ToolHelp(self.client, context, player)

        await context.send(embed=await help.get_detailed_help_for(1, "character"))
    
    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @character.command()
    async def info(self, context, reference: int, level=1):
        """Display the character's card"""

        getter = CharacterGetter()

        if level < 1:
            level = 1

        if level > 150:
            level = 150

        character = await getter.get_reference_character(
            reference, self.client, level=level
        )

        card = await character.get_combat_card(self.client, 0)
        
        await context.send(embed=card)
    
    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @character.command()
    async def lock(self, context, unique_id):
        """Allows the player to lock a character he owns"""

        player = Player(context, self.client, context.message.author)

        # If the player wants to lock all the characters
        if unique_id.lower() == "all":
            await self.client.database.execute(
            """
            UPDATE character_unique
            SET locked = true
            WHERE character_owner_id = $1;
            """, [player.id]
            )

            await context.send("✅ You have successfully locked your characters")
            return
        
        # Lock by rarity
        elif unique_id.lower() in self.rarity:
            asked_rarity = await GlobalTool().get_rarity_value(unique_id)
            rarity_icon = await self.icon.get_rarity_icon(asked_rarity)

            await self.client.database.execute(
                """
                UPDATE character_unique
                SET locked = true
                WHERE character_rarity = $1 AND character_owner_id = $2;
                """, [asked_rarity, player.id]
            )

            await context.send(f"✅ You have successfully locked your {rarity_icon} characters")
            return

        # If the player owns the character
        elif await player.item.has_character(unique_id):
            await self.client.database.execute(
                """
                UPDATE character_unique
                SET locked = true
                WHERE character_unique_id = $1;
                """, [unique_id]
            )

            await context.send("✅ You have successfully locked the character")
        
        else:
            await context.send(":x: You do not own this character")
    
    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @character.command()
    async def unlock(self, context, unique_id):
        """Allows the player to unlock a character he owns"""

        player = Player(context, self.client, context.message.author)

        if unique_id.lower() == "all":
            await self.client.database.execute(
            """
            UPDATE character_unique
            SET locked = false
            WHERE character_owner_id = $1;
            """, [player.id]
            )

            await context.send("✅ You have successfully unlocked your characters")
            return
        
        if unique_id.lower() in self.rarity:
            asked_rarity = await self.tool.get_rarity_value(unique_id)
            rarity_icon = await self.icon.get_rarity_icon(asked_rarity)

            await self.client.database.execute(
                """
                UPDATE character_unique
                SET locked = false
                WHERE character_rarity = $1 AND character_owner_id = $2;
                """, [asked_rarity, player.id]
            )

            await context.send(f"✅ You have successfully unlocked your {rarity_icon} characters")
            return

        # If the player owns the character
        elif await player.item.has_character(unique_id):
            await self.client.database.execute(
                """
                UPDATE character_unique
                SET locked = false
                WHERE character_unique_id = $1;
                """, [unique_id]
            )

            await context.send("✅ You have successfully unlocked the character")
        
        else:
            await context.send(":x: You do not own this character")


def setup(client):
    client.add_cog(CommandCharacter(client))
