import discord
from helper import get_settings
from db import update_specific_data
from misc import help_options, option_description


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