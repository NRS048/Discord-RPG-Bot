import discord
import asyncio
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print(f"I am ready to go - {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the dungeon"))

@bot.command()
async def begin(ctx):
    discid = ctx.author.id
    name = ""
    race = ""
    gender = ""
    stealth = 0
    strength = 0
    intelligence = 0
    dexterity = 0

    with open("playerdata.json", 'r') as file:
        data = json.load(file)
        for i in data["player_stats"]:
            if i['discid'] == discid:
                await ctx.send("you already have a game save!")
                file.close()
                return

    try:
        def race_check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["human", "elf", "troll"]

        def gender_check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["male", "female", "other"]

        await ctx.send("what is your character's name?")
        msg = await bot.wait_for("message", timeout=5)
        name = msg.content
        await ctx.send("what is your character's race?")
        await ctx.send("human, elf, troll")
        msg = await bot.wait_for("message", check=race_check, timeout=5)
        race = msg.content.lower()
        await ctx.send("what is your character's gender?")
        await ctx.send("male, female, other")
        msg = await bot.wait_for("message", check=gender_check, timeout=5)
        gender = msg.content.lower()

        await ctx.send("add charachter stat points, must add upp to 50")
        await ctx.send("stealth")
        msg = await bot.wait_for("message", timeout=5)
        stealth = int(msg.content)
        await ctx.send("strength")
        msg = await bot.wait_for("message", timeout=5)
        strength = int(msg.content)
        await ctx.send("intelligence")
        msg = await bot.wait_for("message", timeout=5)
        intelligence = int(msg.content)
        await ctx.send("dexterity")
        msg = await bot.wait_for("message", timeout=5)
        dexterity = int(msg.content)

        if stealth+strength+intelligence+dexterity != 50:
            await ctx.send("the four point catagories did not equal 50 points, resetting begin command")
            return

        def yn_check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y", "n"]

        await ctx.send("are these your settings?")
        await ctx.send(f"y/n: {discid} {name} {race} {gender} {stealth} {strength} {intelligence} {dexterity}")
        msg = await bot.wait_for("message", check=yn_check, timeout=5)
        if msg.content.lower() == "y":
            await ctx.send("saving profile")
            with open("playerdata.json", 'r+') as file:
                data = json.load(file)

                def write_json(new_data):
                    data["player_stats"].append(new_data)
                    file.seek(0)
                    json.dump(data, file, indent = 4)

                y = {
                    "discid": discid,
                     "name": name,
                     "race": race,
                     "gender": gender,
                     "coins": 0,
                     "bounty": 0,
                     "level": 1,
                     "xp": 0,
                     "alignment": 0,
                     "characterstats": {
                         "stealth": stealth,
                         "strength": strength,
                         "intelligence": intelligence,
                         "dexterity": dexterity
                     }
                     "inventory": [0],
                     "skilltree": [0],
                     "worldlocation": [0,0,0],
                     "subsquarelocation": [0,0]
                    }
                write_json(y)
                file.close()
                return
    except asyncio.TimeoutError:
        await ctx.send("Sorry, you didn't reply in time!")
        return

    print(discid, name, race, gender, stealth, strength, intelligence, dexterity)

bot.run(TOKEN)
