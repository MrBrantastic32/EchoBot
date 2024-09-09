import discord
from discord.ext import commands
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

###-Creating Chat Cog-###

class ChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tokenizer = AutoTokenizer.from_pretrained("./trained_model")
        self.model = AutoModelForCausalLM.from_pretrained("./trained_model")

###-Generating the response-###

    def generate_response(self, input_text):
        inputs = self.tokenizer.encode(input_text + self.tokenizer.eos_token, return_tensors="pt")
        outputs = self.model.generate(inputs, max_length=1000, pad_token_id=self.tokenizer.eos_token_id)
        response = self.tokenizer.decode(outputs[:, inputs.shape[-1]:][0], skip_special_tokens=True)
        return response

###-Creating the command-###

    @commands.command(name='chat')
    async def chat(self, ctx, *, user_input: str):
        response = self.generate_response(user_input)
        await ctx.send(response)

###-Uploading the cog-###

async def setup(bot):
    print("cog added")
    await bot.add_cog(ChatCog(bot))
