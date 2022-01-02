import discord
from discord import colour
from discord import embeds
from discord.ext import commands
from discord.ext import tasks
from asyncio import *
from discord.ext.commands.errors import DisabledCommand
import random
from datetime import datetime
from urllib import request
prefix = '!'
TOKEN = "" #Your Token
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=prefix, intents = intents)
client.remove_command("help")
color = [0x0051FF, 0x0042D1, 0xFA73FF, 0x1300D1, 0x00A2D1]


@tasks.loop(seconds=10.0)
async def my_background_task():
    members = 0
    for guild in client.guilds:
        members += guild.member_count - 1
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{members} Members"),status=discord.Status.dnd)

    
@client.event
async def on_ready():
    print('Logged in as: {}'.format(client.user.name))
    print('Bot user: {}'.format(client.user))
    print('----------------------------')
    print('| created : 17/05/2020     |')
    print('| last updated: 1/1/2022 |')
    print('| Developer: RadinPirouz   |')
    print('----------------------------')

    my_background_task.start()
# ----- Admin Command ----- #
@client.command(description = "Clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount = 2):
    await ctx.channel.purge(limit=amount+1)
    embed = discord.Embed(colour=random.choice(color),description=f'{amount} Pyam Pak Shode')
    await ctx.send(embed=embed)
    amount = 1
    await ctx.channel.purge(limit=amount)
    amount = 5  
    
@client.command(description = "Kick Member")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    amount = 1
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(colour=random.choice(color),description=f'{member} Kick Shod')
    await ctx.send(embed=embed)
    
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    amount = 1
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(colour=random.choice(color),description=f'{member} Ban Shod')
    await ctx.send(embed=embed)
    
@client.command()
@commands.has_permissions(manage_messages=True)
async def announce(ctx, *, input2):
    amount = 1
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(colour=random.choice(color),description=input2)
    await ctx.send(embed=embed)
    
@client.command(description="Mutes the specified user.")
@commands.has_permissions(administrator=True)
async def mute(cdv, member: discord.Member, *, reason=None):
    guild = cdv.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False, connect=False)
    await member.add_roles(mutedRole, reason=reason)
    await cdv.send(f"Muted {member.mention} for reason {reason}")
    await member.send(f"Sho{guild.name} for {reason}")
    
@client.command(description="Unmutes a specified user.")
@commands.has_permissions(administrator=True)
async def unmute(cdv, member: discord.Member):
    mutedRole = discord.utils.get(cdv.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await cdv.send(f"Unmuted {member.mention}")
    await member.send(f"You were unmuted in the server {cdv.guild.name}")

@client.command()
@commands.has_permissions(administrator=True)
async def warn(ctx,member: discord.Member,*,result):
    authorm = ctx.message.author
    embed = discord.Embed(title = "New Warn",colour=random.choice(color),description=f"Warn Be **{member}** Be Dalil **{result}** Dadeshod")
    await ctx.send(embed=embed)
    embed = discord.Embed(title = "New Warn",colour=random.choice(color),description=f"Shoma Tavasot **{authorm}** Be Dalil **{result}** Warn Gereftid")
    await member.send(embed=embed)
    
    

# ----- Developer Command ----- #

@client.command()
@commands.has_permissions(administrator=True)
async def dmsend(cdv, member: discord.Member,*, res):
    embed = discord.Embed(colour=random.choice(color),description=f"Payam Baraye  {member.mention} Ferstade Shod ")
    await cdv.send(embed=embed)
    await member.send(res)
    
@client.command()
@commands.has_permissions(administrator=True)
async def updating(ctx):
    await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="Updating Bot"))
    embed = discord.Embed(colour=random.choice(color),description=f"Bot be Halat Updating Raft")
    await ctx.send(embed=embed)
@client.command()
@commands.has_permissions(administrator=True)
async def resetstatus(ctx):
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="RadinPirouz"))
    embed = discord.Embed(colour=random.choice(color),description=f"Bot Az Halat Updating Dar Amad")
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def datauser(ctx, member: discord.Member):
    created_at = member.created_at.strftime("%b %d, %Y")
    embed = discord.Embed(colour=random.choice(color),description=f"In Account Dar Tarikh {created_at} Sakhte Shode Ast")
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    embed = discord.Embed(colour=random.choice(color),description=f' Ping Bot Is :{round(client.latency * 1000)}MS')
    await ctx.send(embed=embed)

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Help <a:watermelon:902934535040274452>", colour=random.choice(color))
    embed.add_field(name="!ban", value="```❌بن کردن پلیر مورد نظر❌```", inline=True)
    embed.add_field(name="!kick", value="```❌کیک کردن پلیر مورد نظر❌```", inline=True)
    embed.add_field(name="!mute", value="```❗گرفتن درسترسی پلیر به چنل ها❗```", inline=True)
    embed.add_field(name="!unmute",value="```🟩آزاد کردن دسترسی های پلیر🟩```", inline=True)
    embed.add_field(name="!announce",value="```📢انانس زدن در چنل📢```", inline=True)
    embed.add_field(name="!warn",value="```❌وارن دادن به ممبر مورد نظر❌```", inline=True)
    embed.add_field(name="!dmsend", value="```💣فرستادن پیام از طریق بات برای فرد مورد نظر💣```", inline=True)
    embed.add_field(name="!datauser",value="```📅گرفتن تاریخ ساخته شدن اکانت مورد نظر📅```", inline=True)
    embed.add_field(name="!clear",value="```🧧پاک کردن پیام ها در یک چنل🧧```", inline=True)
    embed.add_field(name="!ping", value="```🔓گرفتن پینگ بات🔓```", inline=True)
    await ctx.send(embed=embed)


client.run(TOKEN)
