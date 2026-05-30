import discord
from discord import ui

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