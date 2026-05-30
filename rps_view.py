from __future__ import annotations
import discord


def determine_winner(a, b):
    if a == b:
        return "Draw!"

    wins = {
        ("Rock", "Scissors"),
        ("Scissors", "Paper"),
        ("Paper", "Rock")
    }

    if (a, b) in wins:
        return "Player 1 wins!"

    return "Player 2 wins!"


class RPSView(discord.ui.View):
    def __init__(self, player1, player2):
        super().__init__(timeout=60)

        self.player1 = player1
        self.player2 = player2

        self.choice1 = None
        self.choice2 = None

    async def make_choice(
        self,
        interaction: discord.Interaction,
        choice: str
    ):
        if interaction.user == self.player1:
            self.choice1 = choice
        elif interaction.user == self.player2:
            self.choice2 = choice
        else:
            await interaction.response.send_message(
                "You're not playing.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"You selected {choice}",
            ephemeral=True
        )

        if self.choice1 and self.choice2:
            await self.finish(interaction)

    async def finish(self, interaction):
        result = determine_winner(
            self.choice1,
            self.choice2
        )

        await interaction.followup.send(
            f"{self.player1.mention}: {self.choice1}\n"
            f"{self.player2.mention}: {self.choice2}\n\n"
            f"{result}"
        )

        self.stop()

    @discord.ui.button(
        label="Rock",
        style=discord.ButtonStyle.primary
    )
    async def rock(self, interaction, button):
        await self.make_choice(interaction, "Rock")

    @discord.ui.button(
        label="Paper",
        style=discord.ButtonStyle.primary
    )
    async def paper(self, interaction, button):
        await self.make_choice(interaction, "Paper")

    @discord.ui.button(
        label="Scissors",
        style=discord.ButtonStyle.primary
    )
    async def scissors(self, interaction, button):
        await self.make_choice(interaction, "Scissors")

