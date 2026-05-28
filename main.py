import discord
import os
token = os.getenv("CAMPBOT_TOKEN")
if token is None:
    raise RuntimeError("Missing CAMPBOT_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

synced = False

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

client.run(token)

#lil int 6193533967284288