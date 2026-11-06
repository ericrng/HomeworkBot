import discord
import os
import ast
from discord.ext import commands
from discord import app_commands, SelectOption
from dotenv import load_dotenv
from db import get_specific_data, get_all_data_in_column, get_all_data_in_table, insert_specific_data, \
    update_specific_data, delete_specific_data, reset_specific_data, connect_db, check_existence, insert_many_data, \
    get_dynamic_data, delete_dynamic_data, delete_dynamic_data, get_singular_by_many, update_singular_by_many, \
    get_data_by_value, get_many_by_many, get_many_by_singular, get_data_by_column_value
from datetime import datetime as dt
from helper import get_settings, auto_delete_function, auto_sync_function, insert_periods, check_single_insert, check_single_delete, datetime_check

connect_db()
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="/", intents=intents)
tree = app_commands.CommandTree(client)
WHITELIST = int(os.getenv("AUTHORIZED_USER"))
DISCORD_TOKEN = str(os.getenv("DISCORD_TOKEN"))


class Settings(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)
    @discord.ui.button(label="Change Auto-Sync", style=discord.ButtonStyle.blurple)
    async def change_auto_sync(self, interaction, button):
        current_sync_settings = get_settings(interaction.user.id)[0]
        update_specific_data("user_settings", "auto_sync", not current_sync_settings, interaction.user.id, "user_id")
        await interaction.response.send_message(content="Successfully changed sync settings.", ephemeral=True)
    @discord.ui.button(label="Change Auto-Delete", style=discord.ButtonStyle.blurple)
    async def change_auto_delete(self, interaction, button):
        current_delete_settings = get_settings(interaction.user.id)[1]
        update_specific_data("user_settings", "auto_delete", not current_delete_settings, interaction.user.id, "user_id")
        await interaction.response.send_message(content="Successfully changed delete settings.", ephemeral=True)
    @discord.ui.button(label="Change Visibility Settings", style=discord.ButtonStyle.blurple)
    async def change_visibility_settings(self, interaction, button):
        current_visibility_settings = get_settings(interaction.user.id)[2]
        update_specific_data("user_settings", "visible_homework", not current_visibility_settings, interaction.user.id, "user_id")
        await interaction.response.send_message(content="Successfully changed visibility settings.", ephemeral=True)


# Very repetitive, requires refactoring later.
class HelpOptions(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="/insert_class_periods", description="Admin Command", value="1"),
            discord.SelectOption(label="/insert_class_names", description="Admin Command", value="2"),
            discord.SelectOption(label="/insert_teacher_names", description="Admin Command", value="3"),
            discord.SelectOption(label="/remove_periods", description="Admin Command", value="4"),
            discord.SelectOption(label="/remove_class_names", description="Admin Command", value="5"),
            discord.SelectOption(label="/remove_teacher_names", description="Admin Command", value="6"),
            discord.SelectOption(label="/show_class_periods", description="Display Command", value="7"),
            discord.SelectOption(label="/show_class_names", description="Display Command", value="8"),
            discord.SelectOption(label="/show_teacher_names", description="Display Command", value="9"),
            discord.SelectOption(label="/show_homework", description="HW Command", value="10"),
            discord.SelectOption(label="/add_homework", description="HW Command", value="11"),
            discord.SelectOption(label="/remove_homework", description="HW Command", value="12"),
            discord.SelectOption(label="/change_homework_status", description="HW Command", value="13"),
            discord.SelectOption(label="/settings", description="Settings Command", value="14"),
            discord.SelectOption(label="/change_settings", description="Settings Command", value="15"),
            discord.SelectOption(label="/show_schedule", description="Sync Command", value="16"),
            discord.SelectOption(label="/insert_into_schedule", description="Sync Command", value="17"),
            discord.SelectOption(label="/remove_from_schedule", description="Sync Command", value="18")
        ]
        super().__init__(placeholder="What command do you need help with?", min_values=1, max_values=1, options=options)

    async def callback(self, interaction):
        print(self.values[0])
        embed = discord.Embed()
        match self.values[0]:
            case "1":
                embed = discord.Embed(title="What is /insert_class_periods?", color=discord.Color.blurple())
                embed.add_field(name="\u200b", value="This command allows the administrator to add valid periods, which defines valid data for commands relying on periods.")
            case "2":
                embed = discord.Embed(title="What is /insert_class_names?", color=discord.Color.blurple())
                embed.add_field(name="\u200b", value="This command allows the administrator to add valid class names, which defines valid data for commands relying on class names.")
            case "3":
                embed = discord.Embed(title="What is /insert_teacher_names?", color=discord.Color.blurple())
                embed.add_field(name="\u200b", value="This command allows the administrator to add valid teacher names, which defines valid data for commands relying on teacher names.")
            case "4":
                embed = discord.Embed(title="What is /remove_periods?", color=discord.Color.blurple())
                embed.add_field(name="\u200b", value="This command allows the administrator to remove valid periods from current valid periods.")
            case "5":
                embed = discord.Embed(title="What is /remove_class_names?", color=discord.Color.blurple())
                embed.add_field(name="\u200b", value="This command allows the administrator to remove class names from current valid class names.")
            case "6":
                embed = discord.Embed(title="What is /remove_teacher_names?", color=discord.Color.blurple())
                embed.add_field(name="\u200b", value="This command allows the administrator to remove teacher names from current valid teacher names.")
            case "7":
                embed = discord.Embed(title="What is /show_class_periods?", color=discord.Color.blurple())
                embed.add_field(name="\u200b", value="This command shows all valid periods in an embed.")
            case "8":
                embed = discord.Embed(title="What is /show_class_names?", color=discord.Color.blurple())
                embed.add_field(name="\u200b", value="This command shows all valid classes in an embed.")
            case "9":
                embed = discord.Embed(title="What is /show_teacher_names", color=discord.Color.blurple())
                embed.add_field(name="\u200b", value="This command shows all valid teacher names in an embed.")
            case "10":
                embed = discord.Embed(title="What is /show_homework?", color=discord.Color.blurple())
                embed.add_field(name="\u200b", value="This command shows all your entered (meaning using /add_homework) homeworks in an embed.")
            case "11":
                embed = discord.Embed(title="What is /add_homework?", color=discord.Color.blurple())
                embed.add_field(name="\u200b", value="This command adds a homework to your to-do list (viewable via /show_homework). Must enter parameters such as class name, teacher, period, and due date. Valid data is shown using the show commands.")
            case "12":
                embed = discord.Embed(title="What is /remove_homework?", color=discord.Color.blurple())
                embed.add_field(name="\u200b", value="This command removes a homework from your to-do list (viewable via /show_homework). Selects homework via the parameters in /show_homework. ")
            case "13":
                embed = discord.Embed(title="What is /change_homework_status?", color=discord.Color.blurple())
                embed.add_field(name="\u200b", value="This command changes the status of a homework from your to-do list (either completed or incomplete). Must enter parameters of said homework, found via /show_homework.")
            case "14":
                embed = discord.Embed(title="What is /settings?", color=discord.Color.blurple())
                embed.add_field(name="\u200b", value="This command shows your current settings statuses.")
            case "15":
                embed = discord.Embed(title="What is /change_settings?", color=discord.Color.blurple())
                embed.add_field(name="\u200b", value="This command changes your current settings statuses (click on a button to change).")
            case "16":
                embed = discord.Embed(title="What is /show_schedule?", color=discord.Color.blurple())
                embed.add_field(name="\u200b", value="This command shows your current schedule. Schedule is used for auto-syncing. (Auto-syncing is when someone w/ the same schedule adds homework and it automatically adds to your to-do list.)")
            case "17":
                embed = discord.Embed(title="What is /insert_into_schedule?", color=discord.Color.blurple())
                embed.add_field(name="\u200b", value="This command inserts one period of your day into the schedule (used for auto-syncing ref: show_schedule).")
            case "18":
                embed = discord.Embed(title="What is /remove_from_schedule?", color=discord.Color.blurple())
                embed.add_field(name="\u200b", value="This command removes one period of your day from the schedule.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class HelpMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(HelpOptions())


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}!")
    await tree.sync()
    print("We have synced commands!")


# Allows for owner to set parameters for periods.
@tree.command(name="insert_class_periods", description="Inserts valid class periods.")
@app_commands.describe(start="When does the school day begin?", end="When does the school day end?")
async def insert_class_periods(interaction, start: int, end: int):
    if interaction.user.id == WHITELIST:
        if insert_periods(start, end):
            await interaction.response.send_message(content=f"Successfully inserted periods {start} to {end}!", ephemeral=True)
        else:
            await interaction.response.send_message(content="End period must be greater than start period and start period cannot be less than 1.", ephemeral=True)
    else:
        await interaction.response.send_message(content="You do not have permission to use this command.", ephemeral=True)


@tree.command(name="show_class_periods", description="Gives you a list of all valid class periods.")
async def show_class_periods(interaction):
    periods = get_all_data_in_table("valid_periods")
    embed = discord.Embed(title="All class periods:", color=discord.Color.green())
    for period in periods:
        embed.add_field(name=f"Period {period[0]}", value="\u200b", inline=False)
    await interaction.response.send_message(embed=embed)


@tree.command(name="insert_class_names", description="Insert valid class names.")
@app_commands.describe(class_name="What is the name of the class?")
async def insert_class_name(interaction, class_name: str):
    if interaction.user.id == WHITELIST:
        if check_single_insert("valid_names", "class_name", class_name):
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
        embed.add_field(name=f"{class_name[1]}", value="\u200b", inline=False)
    await interaction.response.send_message(embed=embed)


@tree.command(name="insert_teacher_names", description="Insert valid teacher names.")
@app_commands.describe(teacher_name="What is the name of the teacher?")
async def insert_teacher_name(interaction, teacher_name: str):
    if interaction.user.id == WHITELIST:
        if check_single_insert("valid_teachers", "class_teacher", teacher_name):
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
        embed.add_field(name=f"{teacher_name[1]}", value="\u200b", inline=False)
    await interaction.response.send_message(embed=embed)


@tree.command(name="remove_teacher_names", description="Remove valid teacher names.")
@app_commands.describe(teacher_name="What is the name of the teacher?")
async def remove_teacher_name(interaction, teacher_name: str):
    if interaction.user.id == WHITELIST:
        if check_single_delete("valid_teachers", "class_teacher", teacher_name):
            await interaction.response.send_message(content=f"Successfully deleted teacher name {teacher_name}!", ephemeral=True)
        else:
            await interaction.response.send_message(content="This teacher name does not exist!", ephemeral=True)
    else:
        await interaction.response.send_message(content="You do not have permission to use this command.", ephemeral=True)


@tree.command(name="remove_class_names", description="Remove valid class names.")
@app_commands.describe(class_name="What is the name of the class?")
async def remove_class_name(interaction, class_name: str):
    if interaction.user.id == WHITELIST:
        if check_single_delete("valid_names", "class_name", class_name):
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
@app_commands.describe(homework_name="What is the name of the homework?", class_name="What class is this homework from?", class_teacher="Who is the teacher of this class?", period="What period is this homework from?")
async def add_homework(interaction, homework_name: str, class_name: str, class_teacher: str, period: int, due_date: str):
    data_columns = ("user_id", "homework_name", "class_name", "class_teacher", "class_period", "due_date")
    value_columns = [(interaction.user.id, homework_name, class_name, class_teacher, period, due_date)]
    valid_periods, valid_classes, valid_teachers = get_all_data_in_table("valid_periods"), get_all_data_in_column("valid_names", "class_name"), get_all_data_in_column("valid_teachers", "class_teacher")
    formatted_periods, formatted_classes, formatted_teachers = (period,), (class_name,), (class_teacher,)
    # Checks if due date is before current date or ahead of current date.
    match datetime_check(due_date):
        case True:
            pass
        case False:
            await interaction.response.send_message(content="You cannot have a due-date that is in the past!", ephemeral=True)
            return
        case None:
            await interaction.response.send_message(content="Invalid due date format! *(Hint: m/d/yyyy)*", ephemeral=True)
            return
    # Checks if it is a real period, class, or teacher.
    if formatted_periods not in valid_periods or formatted_classes not in valid_classes or formatted_teachers not in valid_teachers:
        await interaction.response.send_message(content="The parameters of this homework are not valid!", ephemeral=True)
        return
    # Checks if the homework already exists (in which case we ignore.)
    if get_dynamic_data("homework_data", data_columns, value_columns):
        await interaction.response.send_message(content="This homework already exists!", ephemeral=True)
    else:
        insert_many_data("homework_data", data_columns, value_columns)
        # Get the user id's of people who have the same user data.
        data_columns = ("class_period", "class_teacher", "class_name")
        value_columns = [(period, class_teacher, class_name)]
        # Auto-Sync Feature
        for users in get_many_by_many("user_data", data_columns, value_columns, "user_id"):
            print(get_many_by_many("user_data", data_columns, value_columns, "user_id"))
            # Indexing makes this harder to read.
            if users[0] != interaction.user.id:
                auto_sync_function(get_settings(users[0])[0], ("user_id", "homework_name", "class_name", "class_teacher", "class_period", "due_date"), [(users[0], homework_name, class_name, class_teacher, period, due_date)])
        await interaction.response.send_message(content="Successfully inserted homework!", ephemeral=True)


@tree.command(name="show_homework", description="Shows you your to-do list!")
async def show_homework(interaction):
    auto_delete_function(get_settings(interaction.user.id)[1], interaction.user.id)
    data = get_data_by_value("homework_data", "user_id", interaction.user.id)
    embed_list = []
    embed = discord.Embed(title="All Homework Details:", color=discord.Color.yellow())
    # Checks if any homeworks exist.
    await interaction.response.defer()
    if not data:
        await interaction.followup.send(embed=embed)
    enumerated_data = list(enumerate(data))
    for index, value in enumerated_data:
        # This looks awful with the row indexing, but it works for now (will need to fix later).
        embed.add_field(name=f"{index+1}. Homework Name:", value=f"{value[5]}")
        embed.add_field(name="Class Name:", value=f"{value[4]}")
        embed.add_field(name="Class Teacher:", value=f"{value[3]}")
        embed.add_field(name="Class Period:", value=f"{value[2]}")
        embed.add_field(name="Due Date:", value=f"{value[7]}")
        emoji = "❌" if value[6] is False else "✅"
        embed.add_field(name="Homework Status:", value=f"{emoji}")
        embed.add_field(name="\u200b", value="_", inline=False)
        # Checks if it reaches the embed limit via counting homeworks + Adds the last embed.
        if (index + 1) % 3 == 0 or (index + 1) == len(enumerated_data):
            embed_list.append(embed)
            embed = discord.Embed(title="", color=discord.Color.yellow())
    # Sends the list of embeds.
    for embeds in embed_list:
        await interaction.followup.send(embed=embeds)


@tree.command(name="remove_homework", description="Removes a homework from your to-do list!")
@app_commands.describe(homework_name="What is the name of the homework?", class_name="What class is this homework from?", class_teacher="Who is the teacher of this class?", period="What period is this homework from?")
async def remove_homework(interaction, homework_name: str, class_name: str, class_teacher: str, period: int, due_date: str):
    auto_delete_function(get_settings(interaction.user.id)[1], interaction.user.id)
    data_columns = ("user_id", "homework_name", "class_name", "class_teacher", "class_period", "due_date")
    value_columns = [(interaction.user.id, homework_name, class_name, class_teacher, period, due_date)]
    if not get_dynamic_data("homework_data", data_columns, value_columns):
        await interaction.response.send_message(content="This homework does not exist!", ephemeral=True)
    else:
        delete_dynamic_data("homework_data", data_columns, value_columns)
        await interaction.response.send_message(content="Successfully deleted homework!", ephemeral=True)


@tree.command(name="change_homework_status", description="Changes the status of a homework.")
@app_commands.describe(homework_name="What is the name of the homework?", class_name="What class is this homework from?", class_teacher="Who is the teacher of this class?", period="What period is this homework from?")
async def change_homework_status(interaction, homework_name: str, class_name: str, class_teacher: str, period: int, due_date: str):
    data_columns = ("user_id", "homework_name", "class_name", "class_teacher", "class_period", "due_date")
    value_columns = [(interaction.user.id, homework_name, class_name, class_teacher, period, due_date)]
    # Deletes any homeworks with a due date in the past.
    auto_delete_function(get_settings(interaction.user.id)[1], interaction.user.id)
    # Gets whatever is in data_columns that is equal to value_columns, otherwise returns list.
    if not get_dynamic_data("homework_data", data_columns, value_columns):
        await interaction.response.send_message(content="This homework does not exist!", ephemeral=True)
    else:
        # Checks the current status of homework_status
        current_status = get_singular_by_many("homework_data", data_columns, value_columns, "homework_status")
        # Updates value_columns to pass along to update_singular_by_many to update homework_status
        value_columns = [(not current_status[0], interaction.user.id, homework_name, class_name, class_teacher, period, due_date)]
        update_singular_by_many("homework_data", data_columns, value_columns, "homework_status")
        await interaction.response.send_message(content="Successfully updated homework!", ephemeral=True)


@tree.command(name="info", description="Provides basic info about HomeworkBot!")
async def info(interaction):
    embed = discord.Embed(title="What is HomeworkBot?",color=discord.Color.blurple(), description="**HomeworkBot** is a Discord Bot built for those who run **School Discord Servers**. "
                                                                                                  "Its primary function is to act as a **better to-do list for students**."
                                                                                                  " It can (will be able to in the future) **assign homework automatically** to you from your classmates who use this bot."
                          )
    embed.add_field(name="Admin Commands", value="There are currently 6 admin commands and they allow whomever is hosting this bot to **modify the valid periods, valid classes, and valid teacher names**.", inline=False)
    embed.add_field(name="Homework Commands", value="There are 7 rudimentary homework commands: **add, remove, show, and change status**. These can be used by **anyone** (though for the show command, it currently only **supports 3 homeworks**.)", inline=False)
    embed.add_field(name="Future Commands", value="HomeworkBot is still **under development** (therefore **bugs should be expected**) and new commands will be added such as the ability to **sync your to-do lists** with others.", inline=False)
    await interaction.response.send_message(embed=embed)


# Shows settings in an embed.
@tree.command(name="settings", description="Provides your settings information on HomeworkBot!")
async def settings(interaction):
    embed = discord.Embed(title="User Settings:", color=discord.Color.orange())
    auto_sync, auto_delete, visible_homework = get_settings(interaction.user.id)
    embed.add_field(name="Auto Sync:", value=auto_sync, inline=True)
    embed.add_field(name="Auto Delete:", value=auto_delete, inline=True)
    embed.add_field(name="Visible Homework:", value=visible_homework, inline=True)
    await interaction.response.send_message(embed=embed)


# Outputs buttons to click to change settings.
@tree.command(name="change_settings", description="Changes your settings information on HomeworkBot!")
async def change_settings(interaction):
    await interaction.response.send_message(content="Click to Change Settings:", view=Settings(), ephemeral=True)


@tree.command(name="insert_into_schedule", description="Inserts part of your schedule into HomeworkBot! (Necessary for Auto-Sync)")
@app_commands.describe(class_period="What period is this?", class_teacher="What teacher is this?", class_name="What class is this?")
async def insert_schedule(interaction, class_period: int, class_teacher: str, class_name: str):
    if class_period < 1:
        await interaction.response.send_message(content="You can't have a period less than one!", ephemeral=True)
    if (class_period,) in get_all_data_in_table("valid_periods") and (class_teacher,) in get_all_data_in_column("valid_teachers", "class_teacher") and (class_name,) in get_all_data_in_column("valid_names", "class_name"):
        # Checks if something has already been set in the schedule.
        if get_dynamic_data("user_data", ("user_id", "class_period"), [(interaction.user.id, class_period)]):
            await interaction.response.send_message("You cannot have two classes in the same period!", ephemeral=True)
        # Cannot have more than one instance of the same teacher and class or auto sync will add multiple homeworks at once.
        elif get_dynamic_data("user_data", ("user_id", "class_teacher", "class_name"), [(interaction.user.id, class_teacher, class_name)]):
            await interaction.response.send_message(content="You can't have the same teacher and same class!", ephemeral=True)
        else:
            insert_many_data("user_data", ("user_id", "class_period", "class_teacher", "class_name"), [(interaction.user.id, class_period, class_teacher, class_name)])
            await interaction.response.send_message(content="Successfully inserted into schedule!", ephemeral=True)
    else:
        await interaction.response.send_message(content="Invalid parameters!", ephemeral=True)


@tree.command(name="show_schedule", description="Shows your schedule on HomeworkBot!")
async def show_schedule(interaction):
    embed = discord.Embed(title="Schedule:", color=discord.Color.green())
    for period in get_all_data_in_column("valid_periods", "class_period"):
        if get_many_by_many("user_data", ("user_id", "class_period"), [(interaction.user.id, period[0])], "user_id"):
            print(get_many_by_many("user_data", ("user_id", "class_period"), [(interaction.user.id, period[0])], "user_id"))
            output = get_data_by_column_value("user_data", ("class_period", "class_teacher", "class_name"), [(interaction.user.id, period[0])], ("user_id", "class_period"))[0][0]
            class_period, class_teacher, class_name = ast.literal_eval(output)
            embed.add_field(name="Period:", value=class_period, inline=True)
            embed.add_field(name="Teacher:", value=class_teacher, inline=True)
            embed.add_field(name="Class:", value=class_name, inline=True)
        else:
            pass
    await interaction.response.send_message(embed=embed)


@tree.command(name="remove_from_schedule", description="Remove your schedule from HomeworkBot!")
@app_commands.describe(class_period="What period do you want to remove?")
async def remove_schedule(interaction, class_period: int):
    if class_period < 1:
        await interaction.response.send_message(content="You can't have a period less than one!", ephemeral=True)
    if class_period > get_all_data_in_column("valid_periods", "class_period")[-1]:
        await interaction.response.send_message(content="You can't have a period after the day ends!", ephemeral=True)
    if (class_period,) in get_all_data_in_column("valid_periods", "class_period"):
        if get_many_by_many("user_data", ("user_id", "class_period"), [(interaction.user.id, class_period)], "user_id"):
            delete_dynamic_data("user_data", ("user_id", "class_period"), [(interaction.user.id, class_period)])
            await interaction.response.send_message(content=f"Successfully deleted period {class_period}!", ephemeral=True)
        else:
            await interaction.response.send_message(content="You can't delete in your schedule where it doesn't exist!", ephemeral=True)
    else:
        await interaction.response.send_message(content="Invalid parameters!", ephemeral=True)

@tree.command(name="help", description="Provides information on commands!")
async def get_help(interaction):
    await interaction.response.send_message(view=HelpMenu(), ephemeral=True)


client.run(DISCORD_TOKEN)