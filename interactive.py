import discord
from discord.ext import tasks
from helper import get_settings
from db import update_specific_data, dict_get_all_data_in_table
from misc import help_options, option_description, feature_options, feature_description
from datetime import datetime as dt


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
    @discord.ui.button(label="Change Auto-DM Settings", style=discord.ButtonStyle.blurple)
    async def change_auto_dm_settings(self, interaction, button):
        current_dm_settings = get_settings(interaction.user.id)[3]
        update_specific_data("user_settings", "auto_dm", not current_dm_settings, interaction.user.id, "user_id")
        await interaction.response.send_message(content="Successfully changed Auto-DM settings.", ephemeral=True)


class HelpOptions(discord.ui.Select):
    def __init__(self):
        options = []
        for option in help_options:
            options.append(discord.SelectOption(label=option, description=option_description[option]))
        super().__init__(placeholder="What command do you need help with?", min_values=1, max_values=1, options=options)

    async def callback(self, interaction):
        embed = discord.Embed(title=f"What is {self.values[0]}?", color=discord.Color.blurple())
        embed.add_field(name="\u200b", value=help_options[self.values[0]])
        await interaction.response.send_message(embed=embed, ephemeral=True)


class HelpMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(HelpOptions())


class FeatureOptions(discord.ui.Select):
    def __init__(self):
        options = []
        for option in feature_options:
            options.append(discord.SelectOption(label=option, description=feature_description[option]))
        super().__init__(placeholder="What features do you need help with?", min_values=1, max_values=1, options=options)

    async def callback(self, interaction):
        embed = discord.Embed(title=f"What is {self.values[0]}?", color=discord.Color.blurple())
        embed.add_field(name="\u200b", value=feature_options[self.values[0]])
        await interaction.response.send_message(embed=embed, ephemeral=True)


class FeatureMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(FeatureOptions())


# Loop for sending DMs when homework is not done.
@tasks.loop(hours=24)
async def timer(client):
    for value in dict_get_all_data_in_table("homework_data"):
        time = dt.now()
        times = dt.strptime(value["due_date"], "%m/%d/%Y")
        if time > times:
            if not value["homework_status"]:
                if not get_settings(value["user_id"])[3]:
                    return
                user = await client.fetch_user(value["user_id"])
                embed = discord.Embed(title="Past Due Homework:", color=discord.Color.red())
                embed.add_field(name="Homework:", value=value["homework_name"], inline=True)
                embed.add_field(name="Due on:", value=value["due_date"], inline=True)
                await user.send(embed=embed)
        else:
            pass