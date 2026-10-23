import discord
import os
from discord.ext import commands
from discord import app_commands
import psycopg2
from dotenv import load_dotenv
from db import get_specific_data, get_all_data_in_column, get_all_data_in_table, insert_specific_data, update_specific_data, delete_specific_data, reset_specific_data, connect_db, check_existence
connect_db()
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="/", intents=intents)
tree = app_commands.CommandTree(client)
WHITELIST = int(os.getenv("AUTHORIZED_USER"))

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}!")
    await tree.sync()
    print("We have synced commands!")

# Allows for owner to set parameters for periods.
@tree.command(name="insert_class_periods", description="Inserts valid class periods.")
@app_commands.describe(start="When does the school day begin?", end="When does the school day end?")
async def insert_class_periods(interaction, start: int, end: int):
    # This if-else statement block needs to be simplified in the future.
    if interaction.user.id == WHITELIST:
        if end > start:
            if start >= 1:
                for i in range(start, end+1):
                    if not check_existence("valid_periods", "class_period", i):
                        insert_specific_data("valid_periods", "class_period", i)
                    else:
                        pass
                await interaction.response.send_message(content=f"Successfully inserted periods {start} to {end}!", ephemeral=True)
            else:
                await interaction.response.send_message(content="Period has to be greater than or equal to 1.", ephemeral=True)
        else:
            await interaction.response.send_message(content="Your end period cannot be less than your start period.", ephemeral=True)
    else:
        await interaction.response.send_message(content="You do not have permission to use this command.", ephemeral=True)


@tree.command(name="show_class_periods", description="Gives you a list of all valid class periods.")
async def show_class_periods(interaction):
    periods = get_all_data_in_table("valid_periods")
    embed = discord.Embed(title="All class periods:", color=discord.Color.green())
    for period in periods:
        int_period = period[0]
        embed.add_field(name=f"Period {int_period}", value="\u200b", inline=False)
    await interaction.response.send_message(embed=embed)


@tree.command(name="insert_class_names", description="Insert valid class names.")
@app_commands.describe(class_name="What is the name of the class?")
async def insert_class_name(interaction, class_name: str):
    if interaction.user.id == WHITELIST:
        if not check_existence("valid_names", "class_name", class_name):
            insert_specific_data("valid_names", "class_name", class_name)
            await interaction.response.send_message(f"Successfully inserted class {class_name}!", ephemeral=True)
        else:
            await interaction.response.send_message(content="Class name already exists!", ephemeral=True)
    else:
        await interaction.response.send_message(content="You do not have permission to use this command.", ephermeral=True)

@tree.command(name="show_class_names", description="Gives you a list of all valid class names.")
async def show_class_names(interaction):
    class_names = get_all_data_in_table("valid_names")
    embed = discord.Embed(title="All class names:", color=discord.Color.red())
    for class_name in class_names:
        str_class_name = class_name[0]
        embed.add_field(name=f"{str_class_name}", value="\u200b", inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="insert_teacher_names", description="Insert valid teacher names.")
@app_commands.describe(teacher_name="What is the name of the teacher?")
async def insert_teacher_name(interaction, teacher_name: str):
    if interaction.user.id == WHITELIST:
        if not check_existence("valid_teachers", "class_teacher", teacher_name):
            insert_specific_data("valid_teachers", "class_teacher", teacher_name)
            await interaction.response.send_message(content="Successfully inserted teacher name!", ephemeral=True)
        else:
            await interaction.response.send_message(content="This teacher name already exists!", ephemeral=True)
    else:
        await interaction.response.send_message(content="You do not have permission to use this command.", ephemeral=True)

@tree.command(name="show_teacher_names", description="Gives you a list of all valid teacher names.")
async def show_teacher_names(interaction):
    teacher_names = get_all_data_in_table("valid_teachers")
    embed = discord.Embed(title="All teacher names:", color=discord.Color.blue())
    for teacher_name in teacher_names:
        str_teacher_nane = teacher_name[0]
        embed.add_field(name=f"{str_teacher_nane}", value="\u200b", inline=False)
    await interaction.response.send_message(embed=embed)


client.run(str(os.getenv("DISCORD_TOKEN")))