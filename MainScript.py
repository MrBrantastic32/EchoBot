import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv
import os

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


