import discord
from discord.ext import commands
from discord import app_commands, ui
from dotenv import load_dotenv
import os
import json
from ReportModal import ReportModal

# report related shit
reports_file_path = "reports.json"

report_data = {
    "count": 0,
    "id": 0,
    "pending": [],
    "reports": []
}
def load_reports():
    global report_data
    if os.path.exists(reports_file_path):
        try:
            with open(reports_file_path, "r", encoding = "utf-8") as f:
                report_data = json.load(f)
        except Exception as e:
            print(f"Error loading reports: {e}")

load_reports()

# Intents are required
intents = discord.Intents.default()
intents.message_content = True  # For prefix commands
intents.members = True          # If you need member info

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

# Create the bot instance
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)  # Remove default help if custom

@bot.event
async def on_ready():
    await bot.load_extension("cogs.commands")
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.tree.sync()

@bot.event
async def on_message(message:discord.Message):
    if message.mentions and message.mentions[0].id == 1507794999352234114:
        print(message.content)
        content = message.content.strip()
        bot_mention = f"<@{bot.user.id}>"
        bot_mention2 = f"<@!{bot.user.id}>"

        if content.startswith(bot_mention):
            clean_content = content[len(bot_mention):].strip()
        elif content.startswith(bot_mention2):
            clean_content = content[len(bot_mention2):].strip()
        else:
            return
        
        message.content = clean_content
        bot.process_commands(message)









bot.run(token)