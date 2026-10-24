import discord
import os
from discord.ext import commands
from discord import app_commands
import psycopg2
from dotenv import load_dotenv
from db import get_specific_data, get_all_data_in_column, get_all_data_in_table, insert_specific_data, update_specific_data, delete_specific_data, reset_specific_data, connect_db, check_existence, insert_many_data

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


@tree.command(name="remove_teacher_names", description="Remove valid teacher names.")
@app_commands.describe(teacher_name="What is the name of the teacher?")
async def remove_teacher_name(interaction, teacher_name: str):
    if interaction.user.id == WHITELIST:
        if check_existence("valid_teachers", "class_teacher", teacher_name):
            delete_specific_data("valid_teachers", teacher_name, "class_teacher")
            await interaction.response.send_message(content=f"Successfully deleted teacher name {teacher_name}!", ephemeral=True)
        else:
            await interaction.response.send_message(content="This teacher name does not exist!", ephemeral=True)
    else:
        await interaction.response.send_message(content="You do not have permission to use this command.", ephemeral=True)


@tree.command(name="remove_class_names", description="Remove valid class names.")
@app_commands.describe(class_name="What is the name of the class?")
async def remove_class_name(interaction, class_name: str):
    if interaction.user.id == WHITELIST:
        if check_existence("valid_names", "class_name", class_name):
            delete_specific_data("valid_names", class_name, "class_name")
            await interaction.response.send_message(content=f"Successfully deleted class name {class_name}!", ephemeral=True)
        else:
            await interaction.response.send_message(content="This class does not exist!", ephemeral=True)
    else:
        interaction.response.send_message(content="You do not have permission to use this command.", ephemeral=True)


@tree.command(name="remove_periods", description="Remove valid periods.")
@app_commands.describe(period="What is the name of this period?")
async def remove_periods(interaction, period: int):
    if interaction.user.id == WHITELIST:
        if check_existence("valid_periods", "class_period", period):
            delete_specific_data("valid_periods", period, "class_period")
            await interaction.response.send_message(content=f"Successfully deleted period {period}!", ephemeral=True)
        else:
            await interaction.response.send_message(content="This period does not exist!", ephemeral=True)
    else:
        await interaction.response.send_message(content="You do not have permission to use this command.", ephemeral=True)


@tree.command(name="add_homework", description="Adds a homework to your to-do list!")
@app_commands.describe(homework_name="What is the name of the homework?", class_name="What class is this homework from?", class_teacher="Who is the teacher of this class?", period="What period is this homework from?",)
async def add_homework(interaction, homework_name: str, class_name: str, class_teacher: str, period: int):
    data_columns = ("user_id", "homework_name", "class_name", "class_teacher", "class_period")
    value_columns = [(interaction.user.id, homework_name, class_name, class_teacher, period)]
    insert_many_data("homework_data", data_columns, value_columns)
    await interaction.response.send_message(content="Successfully inserted homework!", ephemeral=True)

client.run(str(os.getenv("DISCORD_TOKEN")))