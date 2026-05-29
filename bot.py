import discord
from discord.ext import commands
from discord import app_commands, ui
from dotenv import load_dotenv
import os
import json

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



class ReportModal(ui.Modal, title="User Report Form"):
    
    reportedid = 0

    reported_user = ui.TextInput(
        label="User ID to report (Don't change)",
        placeholder="123456789012345678",
        required=True,
        max_length=100
    )

    reason = ui.TextInput(
        label="Report Reason",
        placeholder="spam, harassment, toxicity, etc...",
        required=True,
        max_length=200
    )

    context = ui.TextInput(
        label="Context (Optional)",
        placeholder="Explain what happened...",
        style=discord.TextStyle.paragraph,
        required=False,
        max_length=1000
    )

    async def on_submit(self, interaction: discord.Interaction):
        global report_data
        # Get the report channel
        report_channel = interaction.client.get_channel(1508581321210073289)
        
        if not report_channel:
            await interaction.response.send_message("Report channel not found!", ephemeral=True)
            return

        embed = discord.Embed(
            title = f"User Report | ID: {report_data["id"]}",
            color = discord.Color.red()
        )

        embed.add_field(name="Reported By", value=interaction.user.mention, inline=False)
        embed.add_field(name="User Reported", value=bot.get_user(self.reportedid).mention, inline=False)
        embed.add_field(name="Reason", value=self.reason.value, inline=False)
        context_value = self.context.value.strip() if self.context.value else "No context provided"
        embed.add_field(name="Context", value=context_value, inline=False)

        await report_channel.send(embed=embed)  
        await interaction.response.send_message("Your report has been submitted successfully!", ephemeral=True)
        report_data["count"] += 1
        report_data["pending"].append(report_data["id"])
        report_data["reports"].append({"reported":self.reported_user.value, "reason":self.reason.value, "context":context_value})
        report_data["id"] += 1
        with open(reports_file_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent = 4, ensure_ascii = False)
        load_reports()



@bot.tree.command(name = "report", description="Report a user")
@app_commands.default_permissions(administrator=True)
async def report(interaction: discord.Interaction, user: discord.Member):
    """Opens the report modal"""
    
    modal = ReportModal()
    modal.reportedid = user.id
    # Optional: Pre-fill the reported user field with the selected user
    modal.reported_user.default = f"{user.name}"
    
    await interaction.response.send_modal(modal)



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