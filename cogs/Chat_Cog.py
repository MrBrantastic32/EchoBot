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
        print("Deffered response, generating responses...")
        try:
            response = self.generator(prompt, max_length=50, num_return_sequences=1, truncation=True)
            generated_text = response[0]['generated_text']
            print("Generated text:", generated_text) 

###-Creating an Embed-###

            embed = discord.Embed(title = "Echo Response", 
                                  description = generated_text, 
                                  color = discord.Color.purple())
            embed.set_author(name=f"{interaction.user.display_name}: {prompt}",
                              icon_url=interaction.user.display_avatar.url)
            
            await interaction.followup.send(embed=embed) 
        except Exception as e:
            print("Error generating text:", e)  
            await interaction.followup.send("Sorry, something went wrong while generating the response.")  


async def setup(bot):
    print('cog added')
    await bot.add_cog(ChatCog(bot))