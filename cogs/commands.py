import asyncio
import random

import discord
from discord.ext import commands


class Commands:
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        print("listening in another class " + __name__)

    @commands.command(aliases=["hi", "sup", "안녕"])
    async def hello(self):
        """Returns a random hello phrase"""
        choices = ["hi",
                   "ohai",
                   "hello",
                   "안녕",
                   "안녕하세요",
                   "sup",
                   ]
        await self.bot.say(random.choice(choices))

    @commands.command(pass_context=True)
    @commands.has_any_role("whales", "admin")
    async def clear(self, ctx, amount=10):
        """Clears chat"""
        messages = self.bot.logs_from(ctx.message.channel, amount)
        count = 0
        async for msg in messages:
            await self.bot.delete_message(msg)
            if count >= 10:
                count = 0
                # Take a break to help avoid rate limit
                await asyncio.sleep(1)

    @commands.command()
    @commands.has_any_role("whales", "admin")
    async def playing(self, *, game=None):
        """Sets now playing status"""
        await self.bot.change_status(game=game if game is None else discord.Game(name=game))

    @commands.command(no_pm=True)
    async def say(self, *, message=None):
        """Says what you tell it to say"""
        if message is not None:
            await self.bot.say(message)

    @commands.command(aliases=["샤샤샤"])
    async def shyshyshy(self):
        """No Sana No Life."""
        await self.bot.upload("res/shyshyshy.gif", content="샤샤샤")

    @commands.command()
    async def joined(self, member: discord.Member):
        """Says when a member joined."""
        await self.bot.say("{0.name} joined in {0.joined_at}".format(member))

    @commands.command(aliases=["emojis"], pass_context=True)
    async def emoji(self, ctx):
        """Gets the emoji for this server"""
        server = ctx.message.server
        msg = ""
        for e in server.emojis:
            msg = msg + str(e) + " "
        await self.bot.say(msg)

    @commands.command(aliases=["rolleyes", "eyes"])
    async def rollseyes(self):
        message = await self.bot.say(":eyes:")
        for x in range(0, 6):
            await asyncio.sleep(1)
            await self.bot.edit_message(message, "<:flippedEyes:217116949895708672>")
            await asyncio.sleep(1)
            await self.bot.edit_message(message, ":eyes:")

    @commands.group(pass_context=True)
    async def cool(self, ctx):
        """Says if a something is cool."""
        if ctx.invoked_subcommand is None:
            await self.bot.say("No, {0.subcommand_passed} is not cool".format(ctx))

    @cool.command(name="bot")
    async def _bot(self):
        """Is the bot cool?"""
        await self.bot.say("Yes, the bot is cool.")
