import logging
from dotenv import load_dotenv
from glue.discord_bot.bot import Bot
import os
import discord
from discord import app_commands
from glue.discord_bot.groups.project import Project
from typing import Literal
from glue.database.database import Database

# add logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# add variable from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = Bot(intents=intents)

bot.tree.add_command(Project(bot))

# connection to database
db = Database()


@bot.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}', ephemeral=True)


@bot.tree.command()
@app_commands.describe(
    first_value='The first value you want to add something to',
    second_value='The value you want to add to the first value',
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int):
    """Adds two numbers together."""
    await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')


@bot.tree.command()
async def remove_guild(interaction: discord.Interaction):
    """Remove a project"""
    try:
        result = db.delete_server({"server_id": interaction.guild_id})
        await interaction.response.send_message(f'Removed project from database. {result}')
    except Exception as e:
        await interaction.response.send_message(f'Error: {e}')


@bot.tree.command()
# use this decorator to hide commmands from certain users
# https://discordpy.readthedocs.io/en/latest/interactions/api.html?highlight=permissions#discord.app_commands.default_permissions
@discord.app_commands.default_permissions()
@app_commands.describe(fruits='fruits to choose from')
async def fruit(interaction: discord.Interaction, fruits: Literal['apple', 'banana', 'cherry']):
    print("invoked")
    await interaction.response.send_message(f'Your favourite fruit is {fruits}.')

if __name__ == '__main__':
    print("logging in...")
    bot.run(DISCORD_TOKEN)
