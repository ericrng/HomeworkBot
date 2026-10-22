import discord
import os
from discord.ext import commands
from discord import app_commands
import psycopg2
from dotenv import load_dotenv
from db import get_specific_data, get_all_data, insert_specific_data, update_specific_data, delete_specific_data, reset_specific_data, connect_db
connect_db()
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="/", intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}!")
    await tree.sync()
    print("We have synced commands!")

# Allows for owner to set parameters for periods.
@tree.command(name="insert_class_periods", description="Inserts valid class periods.")
@app_commands.describe(start="When does the school day begin?", end="When does the school day end?")
async def insert_class_periods(interaction: discord.Interaction, start: int, end: int):
    if interaction.user.id == int(os.getenv("AUTHORIZED_USER")):
        if end > start:
            if start >= 1:
                for i in range(start, end+1):
                    insert_specific_data("valid_data", "class_period", i)
                await interaction.response.send_message(content=f"Successfully inserted periods {start} to {end}!", ephemeral=True)
            else:
                await interaction.response.send_message(content="Period has to be greater than or equal to 1.", ephemeral=True)
        else:
            await interaction.response.send_message(content="Your end period cannot be less than your start period.", ephemeral=True)
    else:
        await interaction.response.send_message(content="You do not have permission to use this command.", ephemeral=True)


client.run(str(os.getenv("DISCORD_TOKEN")))