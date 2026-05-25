import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

# Intents are required
intents = discord.Intents.default()
intents.message_content = True  # For prefix commands
intents.members = True          # If you need member info

load_dotenv()
token = os.environ["TOKEN"]

# Create the bot instance
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)  # Remove default help if custom

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.tree.sync()

@bot.tree.command(name='hello', description='Says hello!')
async def hello(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(f'Hello, {user.mention}!')

@bot.tree.command(name="report", description="create a report for an user")
@app_commands.default_permissions(administrator=True)
async def report(interaction: discord.Interaction, user: discord.Member):
    test_channel = bot.get_channel(1507810520143630376)
    await test_channel.send("report message test")

# Looking To Play Command Shit
game_options = [
    app_commands.Choice(name="Hollow Knight", value="hk"),
    app_commands.Choice(name="HK Silksong", value="ss"),
    app_commands.Choice(name="Any", value="any")
]
modality = [
    app_commands.Choice(name="Normal SvH", value="svh"),
    app_commands.Choice(name="Roulette Run", value="roulette"),
    app_commands.Choice(name="Twist Hunt", value="twist"),
    app_commands.Choice(name="Anything", value="any")
    ]

@bot.tree.command(name="looking_to_play", description="Ping user about an SvH Run")
@app_commands.choices(game = game_options)
@app_commands.choices(mode = modality)
async def looking_to_play(interaction: discord.Interaction, game: str, mode: str, players: int = 0):
    ltp_channel = bot.get_channel(1495182287032025280)  # Replace with your LTP channel ID
    title = "**Runners and Hunters!**"
    if game == "hk":    game_to_play = "Halownest";             image = "https://cdn2.steamgriddb.com/hero/d979c6b9505f55f29948079c9e4e21ab.jpg";   upper_message=f"{interaction.guild.get_role(1495173908524040313).mention}!"
    elif game == "ss":  game_to_play = "Pharloom";              image = "https://cdn2.steamgriddb.com/hero/56cb1764fd28103317c9cbc01f0e2f25.png";   upper_message=f"{interaction.guild.get_role(1495173704269824160).mention}!"
    else:               game_to_play = "any of the 2 kingdoms"; image = "https://cdn2.steamgriddb.com/hero/c9a82215f8133f873beb8804911eef52.jpg";   upper_message=f"{interaction.guild.get_role(1495173908524040313).mention}! {interaction.guild.get_role(1495173704269824160).mention}!"
    
    if players == 0:
        if mode == "svh":           message = f"{interaction.user.mention} wants to have a **Standard Hunt** in {game_to_play}!"
        elif mode == "roulette":    message = f"{interaction.user.mention} wants to have a **Roulette Run** in {game_to_play}!"
        elif mode == "twist":       message = f"{interaction.user.mention} wants to have a **Twist Hunt** in {game_to_play}!"
        elif mode == "any":         message = f"{interaction.user.mention} wants to have a **Hunt** of any modality in {game_to_play}!"
    else:
        if mode == "svh":           message = f"{interaction.user.mention} wants to have a **Standard Hunt** in {game_to_play}! And he needs {players} players!"
        elif mode == "roulette":    message = f"{interaction.user.mention} wants to have a **Roulette Run** in {game_to_play}! And he needs {players} players!"
        elif mode == "twist":       message = f"{interaction.user.mention} wants to have a **Twist Hunt** in {game_to_play}! And he needs {players} players!"
        elif mode == "any":         message = f"{interaction.user.mention} wants to have a **Hunt** of any modality in {game_to_play}! And he needs {players} players!"

    await ltp_channel.send(upper_message, embed=discord.Embed(title=title, description=message).set_image(url=image))


bot.run(token)