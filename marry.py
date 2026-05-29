import discord
from discord import app_commands

class MarryView(discord.ui.View):
    proposer: discord.Member
    proposed: discord.Member

    def __init__(self, proposer, proposed):
        super().__init__(timeout=120)
        self.proposer = proposer
        self.proposed = proposed

    @discord.ui.button(
        label="Accept",
        style=discord.ButtonStyle.green
    )
    async def accept(
            self: MarryView,
            interaction: discord.Interaction,
            button: discord.ui.Button,
    ):
        if interaction.user != self.proposed:
            await interaction.response.send_message(
                "Not your proposal.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"{self.proposed.mention} accept the proposal!"
        )
        await interaction.response.send_message(
            f"{self.proposer.mention} and {self.proposed.mention} are now married!"
        )

    @discord.ui.button(
        label="Decline",
        style=discord.ButtonStyle.red
    )
    async def decline(
            self: MarryView,
            interaction: discord.Interaction,
            button: discord.ui.Button
    ):
        if interaction.user != self.proposed:
            await interaction.response.send_message(
                "Not your proposal!",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"{self.proposed.mention} declined!"
        )