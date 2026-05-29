import discord
from discord import app_commands
import marry
import os
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

synced = False

tree.add_command(mod_group)
tree.add_command(marry_group)

@client.event
async def on_ready():
    global synced
    if not synced:
        await tree.sync()
        synced = True
        print("Synced commands")

@tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="kill")
async def kill(interaction: discord.Interaction, tokill: discord.Member):
    await interaction.response.send_message(f"Killing {tokill.mention}")

@marry_group.command(name="marry")
async def marry(interaction: discord.Interaction, tomarry: discord.Member):
    sent_user = interaction.user
    view = marry.MarryView(sent_user, tomarry)
    await interaction.response.send_message(f"{sent_user.mention} has proposed to {tomarry.mention}!",
                                            view=view)

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
    await interaction.response.send_message(f"Banning {toban.mention}")
    await toban.ban(reason=reason)

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
    await interaction.response.send_message(f"Kicking {tokick.mention}")
    await tokick.kick(reason=reason)

@mod_group.command(name="unban")
@app_commands.default_permissions(
    ban_members=True
)
async def unban(interaction: discord.Interaction, tounban: discord.Member, reason: str):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message(
            "No permission.",
            ephemeral=True
        )
        return
    await interaction.response.send_message(f"Unbanning {tounban.mention}")
    await tounban.unban(reason=reason)


client.run(token)

#lil int 6193533967284288