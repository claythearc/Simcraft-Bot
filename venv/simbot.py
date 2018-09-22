import discord
import asyncio
from discord.ext import commands
import subprocess
from requests_html import HTML
from pathlib import Path
from bs4 import BeautifulSoup
import os

with open("secret.txt","r") as f:
    secret = f.readline().strip()

bot = commands.Bot(command_prefix='.')
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def source(ctx):
    await ctx.send("Source can be found @ https://github.com/claythearc/Simcraft-Bot/blob/master/venv/simbot.py")
    await ctx.send("Written by Clay The Arc#4649 for bugs / problems.")


@bot.command()
async def simc(ctx, *, username: str):
    print("Called")
    ABIL_NAMES = []
    CLASS_COLORS = {
        "Monk" : (0, 255, 150),
        "Death Knight" : (196, 31, 59),
        "Druid" : (255, 125, 10),
        "Hunter" : (171, 212, 115),
        "Mage" : (64, 199, 235),
        "Paladin" : (245, 140, 186),
        "Priest" : (255, 255, 255),
        "Rogue" : (255, 245, 105),
        "Shaman" : (0, 112, 222),
        "Warlock" : (135, 135, 237),
        "Warrior" : (199, 156, 110),
        "Demonhunter" : (163, 48, 201)
    }

    Output = subprocess.call(["/root/sim2/engine/simc", f"armory=us,thrall,{username}", "html={username}.html",
                              "iterations=10", "calculate_scale_factors=1"])
    try:
        with open(f"{username}.html", encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
    except FileNotFoundError:
        await ctx.send("Healing / Tanking is not currently supported.")
        return 0 
    stats = dict()
    dps = soup.find(id='player1').find("td").get_text()
    img = soup.find(id='player1').find("img")['src']
    classname = soup.find(id='player1').find_all("li")[1]
    classname = classname.get_text().split(" ")[1]
    for idx, x in enumerate(
            soup.find(id='player1').find_all('table', class_='sc mt')[1].find_all("tr")[1].find_all("th")):
        if x.get_text() != '':
            ABIL_NAMES.append(x.get_text())

    for idx, x in enumerate(
            soup.find(id='player1').find_all('table', class_='sc mt')[1].find_all("tr")[3].find_all("td")):
        stats[ABIL_NAMES[idx]] = x.get_text()

    for idx, x in enumerate(soup.find(id='player1').find_all('table', class_='sc mt')[2].find("tr").find_all("td")):
        pawn = x.get_text()

    try:
        stats.pop("AP")
        stats.pop("SP")
        stats.pop("Sta")
    except KeyError:
        pass
    em = discord.Embed(title="Simcraft Results", colour=discord.Color.from_rgb( *CLASS_COLORS[classname] ))
    em.set_author(name=username)
    em.set_thumbnail(url=img)
    em.add_field(name=f"DPS: ", value= dps, inline=False)
    for k,v in stats.items():
        em.add_field(name=k, value=v)
    em.add_field(name="Pawn: ", value=pawn)

    os.remove(f"{username}.html")
    await ctx.send(content=None, embed=em)


bot.run(secret)