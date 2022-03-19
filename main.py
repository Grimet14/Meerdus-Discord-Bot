import random
import json
import aiohttp
import requests
import discord
import config
import youtube_dl
import asyncio
from discord import Member
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands import has_permissions, MissingPermissions
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

#bot's prefix and slash command setup

client = commands.Bot(command_prefix='$')
slash = SlashCommand(client, sync_commands=True)

#main code

#bot's status/presence and message when the bot is ready.

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.idle, activity=discord.Game('Whatching Computech Discord'))
  print("Meerdus Logged On")

# Clean meme command, from r/cleanmemes subreddit.


@slash.slash(
    name="cleanmeme",
    description="Displays a random clean meme from the r/cleanmemes subreddit!",
    guild_ids=[config.guild_id],
)
async def _cleanmeme(ctx: SlashContext):
    embed = discord.Embed(
        title="", description="A random meme for you.", color=(0x0000ff)
    )

    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://www.reddit.com/r/cleanmemes/new.json?sort=hot") as r:
            res = await r.json()
            embed.set_image(
                url=res["data"]["children"][random.randint(0, 25)]["data"]["url"]
            )
            await ctx.send(embed=embed)

# Random number between 1 and 100

@slash.slash(
    name="randomnum",
    description="Display a random number between 1 and 100!",
    guild_ids=[config.guild_id],
)
async def _randomnum(ctx: SlashContext):
    embed = discord.Embed(title="Random Number :thumbsup:", description=(random.randint(1, 101)), color=(0x0000ff))
    await ctx.send(embed=embed)


#server info
@slash.slash(
    name="serverinfo",
    description="Get info about this server!",
    guild_ids=[config.guild_id]
)

async def serverinfo(ctx:SlashContext):
    role_count = len(ctx.guild.roles)

    serverinfoEmbed = discord.Embed(color=0x0000ff)
    serverinfoEmbed.add_field(name='Name', value=f"{ctx.guild.name}", inline=False)
    serverinfoEmbed.add_field(name='Member Count', value=ctx.guild.member_count, inline=False)
    serverinfoEmbed.add_field(name='Verification Level', value=str(ctx.guild.verification_level), inline=False)
    serverinfoEmbed.add_field(name='Highest Role', value=ctx.guild.roles[-2], inline=False)
    serverinfoEmbed.add_field(name='Number of Roles', value=str(role_count), inline=False)

    await ctx.send(embed = serverinfoEmbed)

#bird command
@slash.slash(
    name="birdy",
    description="Display a random bird photo and fact.",
    guild_ids=[config.guild_id]
)
async def birdy(ctx: SlashContext):
    async with aiohttp.ClientSession() as session:
        request = await session.get("https://some-random-api.ml/img/bird")
        birdjson = await request.json()
        request2 = await session.get("https://some-random-api.ml/facts/bird")
        factjson = await request2.json()

        embed = discord.Embed(title="Birdy! :bird:", color=0x0000ff)
        embed.set_image(url=birdjson["link"])
        embed.set_footer(text=factjson["fact"])
        await ctx.send(embed=embed)

#cat command
@slash.slash(
    name="kitty",
    description="Display a random cat photo and fact.",
    guild_ids=[config.guild_id]
)
async def kitty(ctx: SlashContext):
    async with aiohttp.ClientSession() as session:
        request = await session.get("https://some-random-api.ml/img/cat")
        catjson = await request.json()
        request2 = await session.get("https://some-random-api.ml/facts/cat")
        factjson = await request2.json()

        embed = discord.Embed(title="Kitty! :cat:", color=0x0000ff)
        embed.set_image(url=catjson["link"])
        embed.set_footer(text=factjson["fact"])
        await ctx.send(embed=embed)

#dog command
@slash.slash(
    name="doggo",
    description="Display a random dog photo and fact.",
    guild_ids=[config.guild_id]
)
async def doggo(ctx: SlashContext):
    async with aiohttp.ClientSession() as session:
        request = await session.get("https://some-random-api.ml/img/dog")
        dogjson = await request.json()
        request2 = await session.get("https://some-random-api.ml/facts/dog")
        factjson = await request2.json()

        embed = discord.Embed(title="Doggo! :dog:", color=0x0000ff)
        embed.set_image(url=dogjson["link"])
        embed.set_footer(text=factjson["fact"])
        await ctx.send(embed=embed)

# Lock a specified channel (the ability to manage channels is required.)


@slash.slash(
    name="lock",
    description="Lock a specified channel, the ability to manage channels is required.",
    guild_ids=[config.guild_id],
)
@commands.has_permissions(manage_channels=True)
async def lock(ctx: SlashContext, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(":white_check_mark: Channel locked.")


# Unlock a specified channel (the ability to manage channels is required.)


@slash.slash(
    name="unlock",
    description="Unlock a specified channel, the ability to manage channels is required.",
    guild_ids=[config.guild_id],
)
@commands.has_permissions(manage_channels=True)
async def lock(ctx: SlashContext, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(":white_check_mark: Channel unlocked.")

# Coinflip command

determine_flip = [1, 0]


@slash.slash(
    name="coinflip",
    description="Heads or tails, which shall it be?",
    guild_ids=[config.guild_id],
)
async def coinflip(ctx: SlashContext):
    if random.choice(determine_flip) == 1:
        embed = discord.Embed(
            title="Coinflip",
            color=0x0000ff,
            description=f"{ctx.author.mention} Flipped coin, we got **Heads**! :coin:",
        )
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            title="Coinflip",
            color=0x0000ff,
            description=f"{ctx.author.mention} Flipped coin, we got **Tails**! :coin:",
        )
        await ctx.send(embed=embed)

# Kick command


@slash.slash(
    name="kick",
    description="Kick a member, the ability to kick members is required.",
    guild_ids=[config.guild_id],
)
@has_permissions(kick_members=True)
async def kick(ctx: SlashContext, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"User {member} was kicked. :white_check_mark:")


@kick.error
async def kick_error(ctx: SlashContext, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permissions to kick people.")


# Ban command


@slash.slash(
    name="ban",
    description="Ban a member, the ability to ban members is required.",
    guild_ids=[config.guild_id],
)
@has_permissions(ban_members=True)
async def ban(ctx: SlashContext, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"User {member} was banned. :white_check_mark:")


@ban.error
async def ban_error(ctx: SlashContext, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permissions to ban people.")

# ping pong
@slash.slash(name="ping", description="Pong!", guild_ids=[config.guild_id])
async def ping(ctx: SlashContext):
    embed = discord.Embed(
        title=f":white_check_mark: Pong! Latency: {round(client.latency * 1000)}ms",
        color=0x0000ff,
    )
    await ctx.send(embed=embed)


client.run(config.token)