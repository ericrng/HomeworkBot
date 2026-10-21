import discord
import os
from discord.ext import commands
from discord import app_commands
import psycopg2
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="/", intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}!")


client.run(str(os.getenv("DISCORD_TOKEN")))