import discord
import random
import time
import aiohttp
from discord.ext import commands
from datetime import timedelta
from commands import bot_commands
from cryptography.fernet import Fernet
import os
import json

message_counts = {}
# just edit this potion to add your token
# personally i had it in a .env and encrypted it for fun with fernet
# just add an .env somewhere with your bot token heres an example
DISCORD_TOKEN=(insert token)
#with open(', "rb") as f:
#    key = f.read()

#fernet = Fernet(key)

#with open(r"", "rb") as f:
#    decrypted = fernet.decrypt(f.read()).decode()

#for line in decrypted.splitlines():
#    if "=" in line:
#        k, v = line.split("=", 1)
#        os.environ[k.strip()] = v.strip()

TOKEN = os.environ["DISCORD_TOKEN"]
creatorid = 1254305475898638338

if TOKEN is None:
    print("Error: TOKEN not found. Check your .env file name and variable name.")
else:
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.presences = True
    bot = commands.Bot(command_prefix='$', intents=intents)

    @bot.event
    async def on_ready():
        global message_counts
        try:
            with open('counts.json', 'r') as f:
                message_counts = json.load(f)
        except FileNotFoundError:
            message_counts = {}
        print(f'bot made by d8x44 id:{creatorid}')

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return
        print(f'[{message.channel}] {message.author}: {message.content}')
        if bot.user.mentioned_in(message):
            await message.channel.send(f"freak you {message.author.mention}")
        guild_id = str(message.guild.id) if message.guild else 'dm'
        user_id = str(message.author.id)
        if guild_id not in message_counts:
            message_counts[guild_id] = {}
        if user_id not in message_counts[guild_id]:
            message_counts[guild_id][user_id] = 0
        message_counts[guild_id][user_id] += 1
        with open('counts.json', 'w') as f:
            json.dump(message_counts, f)
        await bot.process_commands(message)

    @bot.command()
    async def leaderboard(ctx):
        guild_id = str(ctx.guild.id)
        if guild_id not in message_counts:
            await ctx.send('no data for this server yet')
            return
        top = sorted(message_counts[guild_id].items(), key=lambda x: x[1], reverse=True)[:10]
        result = "leaderboard\n"
        for i, (user_id, count) in enumerate(top, 1):
            user = bot.get_user(int(user_id))
            name = user.name if user else f"Unknown ({user_id})"
            result += f"{i}. {name} - {count} messages\n"
        await ctx.send(result)

    @bot.command()
    async def scan(ctx):
        if ctx.author.id != creatorid:
            await ctx.send('you cant do that')
            return
        await ctx.send('scanning all messages, this might take a while...')
        count = 0
        for channel in bot.get_all_channels():
            if isinstance(channel, discord.TextChannel):
                guild_id = str(channel.guild.id)
                if guild_id not in message_counts:
                    message_counts[guild_id] = {}
                try:
                    async for message in channel.history(limit=None):
                        if not message.author.bot:
                            user_id = str(message.author.id)
                            if user_id not in message_counts[guild_id]:
                                message_counts[guild_id][user_id] = 0
                            message_counts[guild_id][user_id] += 1
                            count += 1
                except:
                    pass
        with open('counts.json', 'w') as f:
            json.dump(message_counts, f)
        await ctx.send(f'done! scanned {count} messages')

    @bot.command()
    async def ping(ctx):
        await ctx.send('@everyone')

    @bot.command()
    async def dmuser(ctx, member: discord.Member, *args):
        if ctx.author.id == creatorid or friend1:
            messages = ' '.join(args)
            await ctx.send(f'dmed with {member.mention}')
            await member.send(messages)
        else:
            await ctx.send('you arent d8 sorry bud')

    @bot.command()
    async def echo(ctx, *args):
        arguments = ' '.join(args)
        await ctx.send(f'{arguments}')

    @bot.command()
    async def getava(ctx, member: discord.Member):
        await ctx.send(f"{member.mention}'s avatar is: {member.avatar} {ctx.author.mention}")

    @bot.command()
    async def status(ctx, member: discord.Member):
        if member == 'D8X4SBOT':
            await ctx.send('im {member.status}')
        else:
            await ctx.send(f'{member.mention}s status is {member.status}')

    @bot.command()
    async def timeout(ctx, member: discord.Member, seconds: int, *, reason="No reason provided"):
        if ctx.author.id == creatorid:
            try:
                duration = discord.utils.utcnow() + timedelta(seconds=seconds)
                await member.timeout(duration, reason=reason)
                await ctx.send(f'{member.mention} has been timed out for {seconds} seconds(s)!')
            except discord.Forbidden:
                await ctx.send("Bot doesn't have permission to timeout this user!")
            except Exception as e:
                await ctx.send(f"Something went wrong: {e}")

    @bot.command()
    async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
        if ctx.author.id == creatorid or friend1:
            try:
                await member.kick(reason=reason)
                await ctx.send(f'{member.mention} has been kicked out')
            except discord.Forbidden:
                await ctx.send("Bot doesn't have permission to kick this user!")
            except Exception as e:
                await ctx.send(f"Something went wrong; {e}")

    @bot.command()
    async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
        if ctx.author.id == creatorid or friend1:
            try:
                await member.ban(reason=reason)
                await ctx.send(f'{member.mention} has been banned')
            except discord.Forbidden:
                await ctx.send('cant ban this member')
            except Exception as e:
                await ctx.send(f"something went wrong; {e}")

    @bot.command()
    async def rps(ctx, arg):
        choices = ['rock', 'paper', 'scissors']
        choice = random.choice(choices)
        await ctx.send(f'my choice was {choice} yours was {arg}')
        if choice == arg:
            await ctx.send('we tied')
        elif choice == 'rock' and arg == 'paper':
            await ctx.send('i lost.')
        elif choice == 'rock' and arg == 'scissors':
            await ctx.send('i win!')
        elif choice == 'paper' and arg == 'scissors':
            await ctx.send('I lost.')
        elif choice == 'paper' and arg == 'rock':
            await ctx.send('i win!')
        elif choice == 'scissors' and arg == 'rock':
            await ctx.send('i lost.')
        elif choice == 'scissors' and arg == 'paper':
            await ctx.send('i win!')

    @bot.command()
    async def whois(ctx, member: discord.Member):
        await ctx.send(f'{member.mention} is really {member.name}')

    @bot.command()
    async def botping(ctx):
        await ctx.send(f'ping of bot: {bot.latency:.2f}')

    @bot.command(name='commands')
    async def cmdlist(ctx):
        commands_text = '\n'.join(bot_commands)
        await ctx.send(f' commands ; {commands_text}')

    @bot.command()
    async def messagech(ctx, *args):
        try:
            channel = bot.get_channel(1401001060482547905)
            arguments = ' '.join(args)
            await channel.send(arguments)
        except:
            ctx.message(f'{ctx.author.mention} the shit failed')

    @bot.command()
    async def spotify(ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        try:
            for activity in member.activities:
                if isinstance(activity, discord.Spotify):
                    await ctx.send(f'{member.mention} is listening to;')
                    await ctx.send(f'Title: {activity.title}')
                    await ctx.send(f'Artist: {activity.artist}')
                    await ctx.send(f'Album: {activity.album}')
                    await ctx.send(f'URL: {activity.track_url}')
                    return
            await ctx.send(f'{member.mention} is not listening to spotify')
        except:
            await ctx.send('couldnt find it')

    @bot.command()
    async def animegif(ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.otakugifs.xyz/gif/allreactions") as response1:
                getreaction = await response1.json()
                gifchoice = random.choice(getreaction['reactions'])
                async with session.get(f"https://api.otakugifs.xyz/gif?reaction={gifchoice}") as response:
                    getgif = await response.json()
                    await ctx.send(f"{getgif['url']}")

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def catpic(ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.thecatapi.com/v1/images/search') as response:
                data = await response.json()
                picture = data[0]['url']
                await ctx.send(f"KITTY!")
                await ctx.send(f"{picture}")

    @bot.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def roblox(ctx, username):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://users.roblox.com/v1/users/search?keyword={username}&limit=10') as response:
                if response.status == 200:
                    try:
                        data = await response.json()
                        user = data['data'][0]
                        await ctx.send(f"roblox user; {user['name']}")
                        await ctx.send(f"loser ass display name; {user['displayName']}")
                        await ctx.send(f"id; {user['id']}")
                        await ctx.send(f"verified = {user['hasVerifiedBadge']}")
                        await ctx.send(f"needs 30 second cool down for next lookup (stupid ass api)")
                        with open('roblox_lookups.txt', 'a') as f:
                            f.write(f"user: {user['name']} | display: {user['displayName']} | id: {user['id']} | verified: {user['hasVerifiedBadge']}\n")
                    except Exception as e:
                        await ctx.send(f"error : {e}")
                else:
                    await ctx.send(f"roblox api said no: {response.status}")

# add your nasa api key to the .env and uncomment to use
# example for the .env:
# NASA_KEY=(key)
#    @bot.command()
#    async def potd(ctx):
#        async with aiohttp.ClientSession() as session:
#            async with session.get(f'https://api.nasa.gov/planetary/apod?api_key={NASA_KEY}') as response:
#                data = await response.json()
#                await ctx.send(data['title'])
#                await ctx.send(data['url'])

#    @bot.command()
#    async def randnasa(ctx):
#        async with aiohttp.ClientSession() as session:
#           async with session.get(f'https://api.nasa.gov/planetary/apod?api_key={NASA_KEY}&count=1') as response:
#                data = await response.json()
#                picture = data[0]
#                await ctx.send(picture['title'])
#                await ctx.send(picture['url'])

    @roblox.error
    async def roblox_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'try again in {error.retry_after:.0f} seconds')

    bot.run(TOKEN)
