import discord
from discord import app_commands
import marry
import json
import os

from duel_view import DuelAcceptView
from rps_view import RPSView
from storage import load_marriages, save_marriages, MARRIAGE_FILE

token = os.getenv("CAMPBOT_TOKEN")
if token is None:
    raise RuntimeError("Missing CAMPBOT_TOKEN")
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

#mod group
mod_group = discord.app_commands.Group(
    name="mod",
    description="Moderation Commands"
)

#marry group
marry_group = discord.app_commands.Group(
    name="marry",
    description="Marriage related commands"
)

#game group
game_group = discord.app_commands.Group(
    name="game",
    description="Game Commands"
)

tree.add_command(mod_group)
tree.add_command(marry_group)
tree.add_command(game_group)

@client.event
async def on_ready():
    #guild = discord.Object(id=1461404394934501572)
    #tree.copy_global_to(guild=guild)
    await tree.sync()
    print("Synced commands")

@tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="kill")
async def kill(interaction: discord.Interaction, tokill: discord.Member):
    await interaction.response.send_message(f"Killing {tokill.mention}")

@marry_group.command(name="propose")
async def propose(interaction: discord.Interaction, tomarry: discord.Member):
    marriages = load_marriages()
    sent_user = interaction.user
    uid = str(sent_user.id)
    if uid in marriages:
        await interaction.response.send_message(
            "You Are already married you cheater!"
        )
        return
    view = marry.MarryView(sent_user, tomarry)
    await interaction.response.send_message(f"{sent_user.mention} has proposed to {tomarry.mention}!",
                                            view=view)

@marry_group.command(name="divorce")
async def divorce(interaction: discord.Interaction):
    # load marriages
    marriages = load_marriages()
    # verify user is married
    uid = str(interaction.user.id)
    if uid not in marriages:
        await interaction.response.send_message(
            "You are not married.",
            ephemeral=True
        )
        return
    # get partner
    partner_id = marriages[uid]
    partner = interaction.guild.get_member(int(partner_id))

    # remove both sides from data
    del marriages[uid]
    del marriages[partner_id]

    save_marriages(marriages)

    # remove married role
    role = discord.utils.get(interaction.guild.roles, name="married")
    if role:
        await interaction.user.remove_roles(role)
        if partner:
            await partner.remove_roles(role)

    await interaction.response.send_message(
        f"{interaction.user.mention} divorced {partner.mention if partner else 'someone'}"
    )

@marry_group.command(name="info")
async def marry_info(interaction: discord.Interaction, member: discord.Member = None):
    marriages = load_marriages()
    target = member or interaction.user
    uid = str(target.id)
    if uid not in marriages:
        await interaction.response.send_message(
            f"{target.mention} is not married"
        )
        return

    partner_id = marriages[uid]
    partner = interaction.guild.get_member(int(partner_id))
    await interaction.response.send_message(
        f"{target.mention} is married to {partner.mention if partner else 'Unknown'}"
    )

@mod_group.command(name="ban")
@app_commands.default_permissions(
    ban_members=True
)
async def ban(interaction: discord.Interaction, toban: discord.Member, reason: str):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message(
            "No permission.",
            ephemeral=True
        )
        return
    await toban.ban(reason=reason)
    await interaction.response.send_message(f"Banning {toban.mention}")

@mod_group.command(name="kick")
@app_commands.default_permissions(
    kick_members=True
)
async def kick(interaction: discord.Interaction, tokick: discord.Member, reason: str):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message(
            "No permission.",
            ephemeral=True
        )
        return
    await tokick.kick(reason=reason)
    await interaction.response.send_message(f"Kicking {tokick.mention}")

@mod_group.command(name="unban")
@app_commands.default_permissions(
    ban_members=True
)
async def unban(interaction: discord.Interaction, tounban: discord.User, reason: str):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message(
            "No permission.",
            ephemeral=True
        )
        return
    await interaction.guild.unban(tounban, reason=reason)
    await interaction.response.send_message(f"Unbanning {tounban.mention}")

@game_group.command(name="duel")
async def duel(interaction: discord.Interaction, opponent: discord.Member):
    view = DuelAcceptView(
        interaction.user,
        opponent
    )

    await interaction.response.send_message(
        f"{interaction.user.mention} challenged "
        f"{opponent.mention} to a DUEL!",
        view=view
    )

@game_group.command(name="rps")
async def rps(interaction: discord.Interaction, opponent: discord.Member):
    view = RPSView(
        interaction.user,
        opponent
    )

    await interaction.response.send_message(
        f"{interaction.user.mention} challenged "
        f"{opponent.mention} to Rock Paper Scissors!",
        view=view
    )
client.run(token)

#lil int 6193533967284288