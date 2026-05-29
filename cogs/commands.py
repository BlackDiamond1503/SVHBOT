import discord
from discord.ext import commands
from discord import app_commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.tree.add_command