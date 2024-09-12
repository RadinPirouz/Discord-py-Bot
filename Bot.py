import discord
from discord.ext import commands, tasks
import random
from datetime import datetime

prefix = '!'
TOKEN = ""  # Your Token
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=prefix, intents=intents)
client.remove_command("help")

# Predefined Colors for Embeds
colors = [0x0051FF, 0x0042D1, 0xFA73FF, 0x1300D1, 0x00A2D1]

# Helper function to create embed messages
def create_embed(description, color=None):
    return discord.Embed(colour=color or random.choice(colors), description=description)

# Helper function to clear a specified number of messages
async def clear_messages(ctx, amount):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(embed=create_embed(f'{amount} messages cleared'))
    await ctx.channel.purge(limit=1)

# ----- Background Task ----- #
@tasks.loop(seconds=10.0)
async def update_member_count():
    total_members = sum(guild.member_count for guild in client.guilds)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{total_members} Members"), status=discord.Status.dnd)

# ----- Bot Events ----- #
@client.event
async def on_ready():
    print(f'Logged in as: {client.user.name}')
    print(f'Bot user: {client.user}')
    print('----------------------------')
    print('| created : 17/05/2020     |')
    print('| last updated: 1/1/2022   |')
    print('| Developer: RadinPirouz    |')
    print('----------------------------')
    update_member_count.start()

# ----- Admin Commands ----- #
@client.command(description="Clear messages")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 2):
    await clear_messages(ctx, amount)

@client.command(description="Kick Member")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(embed=create_embed(f'{member} has been kicked'))
    await clear_messages(ctx, 1)

@client.command(description="Ban Member")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(embed=create_embed(f'{member} has been banned'))
    await clear_messages(ctx, 1)

@client.command(description="Announce a message")
@commands.has_permissions(manage_messages=True)
async def announce(ctx, *, message):
    await ctx.send(embed=create_embed(message))
    await clear_messages(ctx, 1)

# Mute and Unmute Command
@client.command(description="Mute a user")
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    muted_role = discord.utils.get(guild.roles, name="Muted")
    if not muted_role:
        muted_role = await guild.create_role(name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f"{member.mention} has been muted for {reason}")
    await member.send(f"You were muted in {guild.name} for {reason}")

@client.command(description="Unmute a user")
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(muted_role)
    await ctx.send(f"{member.mention} has been unmuted")
    await member.send(f"You were unmuted in {ctx.guild.name}")

# ----- Developer Commands ----- #
@client.command(description="Send DM to a user")
@commands.has_permissions(administrator=True)
async def dmsend(ctx, member: discord.Member, *, message):
    await member.send(message)
    await ctx.send(embed=create_embed(f'Message sent to {member.mention}'))

@client.command(description="Set bot status to updating")
@commands.has_permissions(administrator=True)
async def updating(ctx):
    await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="Updating Bot"))
    await ctx.send(embed=create_embed(f"Bot is in updating mode"))

@client.command(description="Reset bot status")
@commands.has_permissions(administrator=True)
async def resetstatus(ctx):
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="RadinPirouz"))
    await ctx.send(embed=create_embed(f"Bot status reset"))

@client.command(description="Fetch user creation date")
async def datauser(ctx, member: discord.Member):
    created_at = member.created_at.strftime("%b %d, %Y")
    await ctx.send(embed=create_embed(f"This account was created on {created_at}"))

# ----- General Commands ----- #
@client.command(description="Check bot's latency")
async def ping(ctx):
    latency = round(client.latency * 1000)
    await ctx.send(embed=create_embed(f'Ping: {latency}ms'))

# ----- Help Command ----- #
@client.command(description="Display available commands")
async def help(ctx):
    embed = discord.Embed(title="Help Menu", colour=random.choice(colors))
    embed.add_field(name="!ban", value="Ban a user", inline=True)
    embed.add_field(name="!kick", value="Kick a user", inline=True)
    embed.add_field(name="!mute", value="Mute a user", inline=True)
    embed.add_field(name="!unmute", value="Unmute a user", inline=True)
    embed.add_field(name="!announce", value="Make an announcement", inline=True)
    embed.add_field(name="!warn", value="Warn a user", inline=True)
    embed.add_field(name="!dmsend", value="Send a DM to a user", inline=True)
    embed.add_field(name="!datauser", value="Fetch account creation date", inline=True)
    embed.add_field(name="!clear", value="Clear messages", inline=True)
    embed.add_field(name="!ping", value="Check bot latency", inline=True)
    await ctx.send(embed=embed)

# Start the bot
client.run(TOKEN)
