import discord
from discord.ext import commands
from discord import app_commands
from ReportModal import ReportModal
from ModeEnums import GameModeType, GameType

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cleanup", description="Delete messages")
    @app_commands.default_permissions(manage_messages=True)
    async def cleanup(self, interaction: discord.Interaction, amount: int):

        if amount < 1:
            await interaction.response.send_message("Amount must be at least 1.", ephemeral=True)
            return

        if amount > 1000:
            await interaction.response.send_message("Maximum is 1000 messages.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        try:
            deleted = await interaction.channel.purge(
                limit=amount,
                bulk=True,
                reason=f"Cleanup by {interaction.user}"
            )

            embed = discord.Embed(
                title="Cleanup Complete",
                description=f"Deleted **{len(deleted)}** messages.",
                color=discord.Color.green()
            )

            await interaction.followup.send(embed=embed, ephemeral=True)

        except discord.Forbidden:
            await interaction.followup.send("Missing permissions.", ephemeral=True)

        except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)

    @app_commands.command(name="hello", description="Say hello")
    async def hello(self, interaction: discord.Interaction, user: discord.Member):

        if any(role.name == "Lower ADMIN" for role in interaction.user.roles):
            await interaction.response.send_message(
                f"Hello {user.mention}!"
            )
        else:
            await interaction.response.send_message(
                "No permission.",
                ephemeral=True
            )

    @app_commands.command(name = "report", description="Report a user")
    @app_commands.default_permissions(administrator=True)
    async def report(self, interaction: discord.Interaction, user: discord.Member):
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

    @app_commands.command(name="looking_to_play", description="Ping user about an SvH Run")
    @app_commands.choices(game = game_options)
    @app_commands.choices(mode = modality)
    async def looking_to_play(self, interaction: discord.Interaction, game: str, mode: str, players: int = 0):
        mode_enum_key = next((m for m in GameModeType if m.value.key == mode), GameModeType.ANY.value.key)
        mode_enum_display = next((m.value.display for m in GameModeType if mode_enum_key == mode), GameModeType.ANY.value.display)
        ltp_channel = self.bot.get_channel(1495182287032025280)  # Replace with your LTP channel ID
        title = "**Runners and Hunters!**"
        try:
            game_to_play = next((g.value.display for g in GameType if g.value.key == game), GameType.ANY.value.display)
            
        except ValueError:
            game_to_play = GameType.any.value.key
            
        match game_to_play:
            case "Hallownest":
                image = "https://cdn2.steamgriddb.com/hero/d979c6b9505f55f29948079c9e4e21ab.jpg";   
                upper_message=f"{interaction.guild.get_role(1495173908524040313).mention}!"
            case "Pharloom":
                image = "https://cdn2.steamgriddb.com/hero/56cb1764fd28103317c9cbc01f0e2f25.png";   
                upper_message=f"{interaction.guild.get_role(1495173704269824160).mention}!"
            case "Hallownest or Pharloom":
                image = "https://cdn2.steamgriddb.com/hero/c9a82215f8133f873beb8804911eef52.jpg";  
                upper_message=f"{interaction.guild.get_role(1495173908524040313).mention}! {interaction.guild.get_role(1495173704269824160).mention}!"
            case _:
                image = "https://cdn2.steamgriddb.com/hero/c9a82215f8133f873beb8804911eef52.jpg";  
                upper_message=f"{interaction.guild.get_role(1495173908524040313).mention}! {interaction.guild.get_role(1495173704269824160).mention}!"

        if players == 0:
            #if mode == "svh":           
            #    message = f"{interaction.user.mention} wants to have a **Standard Hunt** in {game_to_play}!"
            #elif mode == "roulette":    
            #    message = f"{interaction.user.mention} wants to have a **Roulette Run** in {game_to_play}!"
            #elif mode == "twist":       
            #    message = f"{interaction.user.mention} wants to have a **Twist Hunt** in {game_to_play}!"
            #elif mode == "any":         
                message = f"{interaction.user.mention} wants to have a {mode_enum_display} in {game_to_play}!"
        else:
            #if mode == "svh":           message = f"{interaction.user.mention} wants to have a **Standard Hunt** in {game_to_play}! And he needs {players} players!"
            #elif mode == "roulette":    message = f"{interaction.user.mention} wants to have a **Roulette Run** in {game_to_play}! And he needs {players} players!"
            #elif mode == "twist":       message = f"{interaction.user.mention} wants to have a **Twist Hunt** in {game_to_play}! And he needs {players} players!"
            #elif mode == "any":         message = f"{interaction.user.mention} wants to have a **Hunt** of any modality in {game_to_play}! And he needs {players} players!"
            message = f"{interaction.user.mention} wants to have a {mode_enum_display} in {game_to_play}! And he needs {players} player(s)!"

        await ltp_channel.send(upper_message, embed=discord.Embed(title=title, description=message).set_image(url=image))


async def setup(bot):
    await bot.add_cog(Commands(bot))
    await bot.tree.sync()