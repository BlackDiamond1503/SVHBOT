import discord
from discord import ui
import Tools

class ReportModal(ui.Modal, title="User Report Form"):
    
    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.report = {}
        self.reporter = Tools.ReportFile("reports.json")

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
        # Get the report channel
        report_channel = interaction.client.get_channel(1508581321210073289)
        
        if not report_channel:
            await interaction.response.send_message("Report channel not found!", ephemeral=True)
            return

        embed = discord.Embed(
            title = "User Report",
            color = discord.Color.red()
        )

        embed.add_field(name="Reported By", value=interaction.user.mention, inline=False)
        embed.add_field(name="User Reported", value=self.bot.get_user(self.reportedid).mention, inline=False)
        embed.add_field(name="Reason", value=self.reason.value, inline=False)
        context_value = self.context.value.strip() if self.context.value else "No context provided"
        embed.add_field(name="Context", value=context_value, inline=False)

        self.report = {"reported":self.reportedid, "reason":self.reason.value, "context":self.context.value, }

        await report_channel.send(embed=embed)  
        await interaction.response.send_message("Your report has been submitted successfully!", ephemeral=True)