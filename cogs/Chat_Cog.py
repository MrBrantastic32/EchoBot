import discord
from discord.ext import commands
from transformers import pipeline
import tensorflow as tf

###-Creating the Chat_Cog-###

class ChatCog(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.generator = pipeline('text-generation', model='gpt2', pad_token_id = 50256)  

    @discord.app_commands.command(name="chat", description="Generate responses from AI")
    async def generate(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        response = self.generator(prompt, max_length=50, num_return_sequences=1, truncation=True)
        await interaction.followup.send_message(response[0]['generated_text'])  

async def setup(bot):
    print('cog added')
    await bot.add_cog(ChatCog(bot))
