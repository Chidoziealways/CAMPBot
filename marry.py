from __future__ import annotations
import discord
from discord import app_commands

from storage import load_marriages, save_marriages


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

        role = discord.utils.get(interaction.guild.roles, name="married")
        if role:
            await self.proposer.add_roles(role)
            await self.proposed.add_roles(role)

        await interaction.response.send_message(
            f"{self.proposed.mention} accept the proposal!"
        )
        await interaction.followup.send(
            f"{self.proposer.mention} and {self.proposed.mention} are now married!"
        )
        marriages = load_marriages()
        u1 = str(self.proposer.id)
        u2 = str(self.proposed.id)
        marriages[u1] = u2
        marriages[u2] = u1

        save_marriages(marriages)

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