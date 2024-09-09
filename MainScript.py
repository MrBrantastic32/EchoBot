import logging
from pathlib import Path
import traceback
import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv
import os
import asyncio
import tensorflow as tf
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

###-Suppress TensorFlow warnings-###

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

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
        await bot.tree.sync()

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

###-Training AI model-###

async def train_model():
    model_name =  "microsoft/DialoGPT-medium"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    dataset = load_dataset("daily_dialog")

    training_args =  TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        save_steps=10_000,
        save_total_limit=2,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
    )

    trainer.train()
    model.save_pretrained("./trained_model")
    tokenizer.save_pretrained("./trained_model")


###-Running Bot-###

async def main():
    async with bot:
        await load_cogs()
        print('cog loaded successfully')
        await train_model()
        await bot.start(Discord_Token)

asyncio.run(main())
