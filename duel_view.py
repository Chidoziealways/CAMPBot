from __future__ import annotations

import asyncio
import random

import discord

class DuelAcceptView(discord.ui.View):
    challenger: discord.Member
    opponent: discord.Member

    def __init__(self, challenger, opponent):
        super().__init__(timeout=180)
        self.challenger = challenger
        self.opponent = opponent

    @discord.ui.button(
        label="Accept",
        style=discord.ButtonStyle.green,
    )
    async def accept(self: DuelAcceptView, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.opponent:
            await interaction.response.send_message(
                "Not your duel.",
                ephemeral=True
            )
            return

        duel = DuelView(
            self.challenger,
            self.opponent
        )

        await interaction.response.send_message(
            "Get ready..."
        )

        await asyncio.sleep(
            random.randint(2, 8)
        )

        await interaction.followup.send(
            "DRAW!!!",
            view=duel
        )

    @discord.ui.button(
        label="Decline",
        style=discord.ButtonStyle.red
    )
    async def decline(
            self: DuelAcceptView,
            interaction: discord.Interaction,
            button: discord.ui.Button
    ):
        if interaction.user != self.opponent:
            await interaction.response.send_message(
                "Not your duel!",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"{self.opponent.mention} declined {self.challenger.mention}'s duel!!"
        )


class DuelView(discord.ui.View):
    challenger = discord.Member
    opponent = discord.Member
    finished: bool = False

    def __init__(self, challenger, opponent):
        super().__init__(timeout=180)
        self.challenger = challenger
        self.opponent = opponent

    @discord.ui.button(
        label="FIRE",
        style=discord.ButtonStyle.red
    )
    async def fire(self: DuelView, interaction: discord.Interaction, button: discord.ui.Button):
        if self.finished:
            await interaction.response.send_message("Too Late!", ephemeral=True)
            return

        if interaction.user not in (
            self.challenger,
            self.opponent
        ):
            await interaction.response.send_message("Not your duel!", ephemeral=True)
            return

        self.finished = True

        await interaction.response.send_message(
            f"{interaction.user.mention} wins the duel!!!"
        )

        self.stop()
