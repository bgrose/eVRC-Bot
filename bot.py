import subprocess
import discord
from discord.ext.commands import Bot
from discord.ext import commands
from mcstatus import MinecraftServer

import asyncio


Client = discord.Client()
client = commands.Bot(command_prefix = "!")

@client.event
async def on_ready():
    print("Bot is ready!")

client.remove_command("help")


def player_count(input):
    index = input.find("players")
    s = input[index:-3]
    max_index = s.find("80")
    count = int(s[9:max_index-1])

    return count


def player_list(input):
    index = input.find("[")

    if index == -1:
        return []

    lst_string = input[index+1:-4]
    lst = lst_string.split(", ")
    lst = [s.split(" ")[0][2:] for s in lst]

    return lst


@client.command()
async def p(ctx):
    server = MinecraftServer.lookup("Vextossup.join-mc.net")
    status = server.status()
    player_count = status.players.online

    output = str(subprocess.check_output("mcstatus Vextossup.join-mc.net status",
                 shell=True))
    players_online = player_list(output)

    if player_count == 0:
        reply = "0 players."
    elif player_count == 1:
        reply = str(player_count) + " player:" + "```" + "\n" + "\n".join(players_online) + "\n" + "```"
    else:
        reply = str(player_count) + " players:" + "```" + "\n" + "\n".join(players_online) + "\n" + "```"

    await ctx.send(reply)


@client.command()
async def help(ctx):
    reply = "```\n" + "Type !p to get a list of the current online players." + "\n```"

    await ctx.send(reply)


@client.event
async def update_game():
    await client.wait_until_ready()

    while True:
        output = str(subprocess.check_output("mcstatus Vextossup.join-mc.net status",
                     shell=True))

        s = str(player_count(output)) + " players online"
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=s))
        await asyncio.sleep(10)


with open("token.txt", "r") as f: #reads text for token
    lines = f.readlines()
    token = lines[0].strip()

# client.loop.create_task(update_game())

client.run(token)
