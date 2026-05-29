import discord
from discord.ext import commands
from discord import app_commands


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


async def setup(bot):
    await bot.add_cog(Commands(bot))
    await bot.tree.sync()