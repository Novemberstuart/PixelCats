import discord
from discord.ext import commands
import os
import json
import random
from PIL import Image

client = commands.Bot(command_prefix = ".")

catparts = {1: {"name":"Body", "value": Image.open("parts/Body1.png")}, 2: {"name":"Ear", "value": Image.open("parts/Ear1.png")}, 3: {"name":"Face", "value": Image.open("parts/Face1.png")}, 4: {"name":"Feet", "value": Image.open("parts/Feet1.png")}, 5:{"name":"Head", "value": Image.open("parts/Head1.png")}, 6:{"name":"Neck", "value": Image.open("parts/Neck1.png")}, 7:{"name":"Tail", "value": Image.open("parts/Tail1.png")}}

pixdata = {}

for x in catparts:
  catvalue = catparts[x]
  catvalue["value"]= catvalue["value"].convert("RGBA")
  catvalue["value"].show()
  pixdata[x] = catvalue["value"].load()

class cat:
  
  def __init__(self, body, ear, face, feet, head, neck, tail, name, profession):

    for x in catparts:
      self.catparts[x] = {"label" : x, "value": ""}

    self.name = ""
    self.profession = "" 

@client.event
async def on_ready():
  print("Ready")

@client.command()
async def start(ctx):
  return

@client.command()
async def test(ctx):
  
  part = {}
  colorpart = {}
  for x in catparts:

    catcolorpart = catparts[x]

    img = catcolorpart["value"]
    img = img.convert("RGBA")

    colorr = random.randint(0, 255)
    colorg = random.randint(0, 255)    
    colorb = random.randint(0, 255)

    pixdata = img.load()

    for y in range(img.size[1]):
      for z in range(img.size[0]):
        if pixdata[z, y] == (255, 255, 255, 255):
          pixdata[z, y] = (colorr, colorg, colorb, 255)
          img.save(f"colorpart{x}.png")

    colorpart[x] = Image.open(f"colorpart{x}.png")

    if x == 1:
      colorpart[x].save("part1.png")
    else:
      catvalue1 = colorpart[x]
      part[x] = Image.alpha_composite(catvalue1, Image.open(f"part{x-1}.png"))
      part[x].show()
      part[x].save(f"part{x}.png")
      part[x].save("newcat.png")

  with open('newcat.png', 'rb') as f:
    picture = discord.File(f)
  await ctx.send(file= picture)

client.run(os.getenv('TOKEN'))