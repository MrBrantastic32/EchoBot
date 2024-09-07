import logging
from pathlib import Path
import traceback
import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv
import os
import asyncio

###-Load env-###

load_dotenv()
Discord_Token = os.getenv('Discord_API_Token')


###-Main Setup-###

class EchoAI(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="/",
            intents=discord.Intents.all()
        )

    async def on_ready(self):
        print("Bot Online!")
        print("------------------------------")
        print(f"Logged in as {self.user} (ID: {self.user.id})")

bot = EchoAI()

###-Loading Cogs-###

async def load_cogs():
    for extension in os.listdir(Path(__file__).parent / "cogs/"):
        if extension.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{extension[:-3]}")
            except Exception:
                logging.error(f"{extension} couldn't be loaded.")
                traceback.print_exc()



load_cogs()
bot.run(Discord_Token)
