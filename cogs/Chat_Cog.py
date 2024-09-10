import discord
from discord.ext import commands
from transformers import pipeline
import re

###-Creating the Chat_Cog-###

class ChatCog(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.generator = pipeline('text-generation', model='gpt2', pad_token_id=50256, eos_token_id=50256)  

###-Truncating sentence-###

    def truncate_to_sentence(self, text):
        match = re.search(r'(.*?)([.!?])(\s|$)', text[::-1])
        if match:
            return text[:len(text) - match.end()]
        return text

    @discord.app_commands.command(name="chat", description="Generate responses from AI")
    async def generate(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        print("Deferred response, generating responses...")
        try:
            response = self.generator(prompt, max_length=100, min_length=1, num_return_sequences=1, 
                                      no_repeat_ngram_size=2, top_p=0.9, temperature=1, early_stopping=True)
            generated_text = response[0]['generated_text']
             
###-Post Processing the text-###
            generated_text = self.truncate_to_sentence(generated_text)
            print("Generated text:", generated_text)

###-Creating an Embed-###

            embed = discord.Embed(title="Echo Response", 
                                  description=generated_text, 
                                  color=discord.Color.purple())
            embed.set_author(name=f"{interaction.user.display_name}: {prompt}",
                             icon_url=interaction.user.display_avatar.url)
            
            await interaction.followup.send(embed=embed) 
        except Exception as e:
            print("Error generating text:", e)  
            await interaction.followup.send("Sorry, something went wrong while generating the response.")  

async def setup(bot):
    print('cog added')
    await bot.add_cog(ChatCog(bot))
