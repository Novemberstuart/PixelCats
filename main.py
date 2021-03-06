import discord
from discord.ext import commands
import os
import json
import random
from PIL import Image
from dotenv import load_dotenv
import numpy as np
load_dotenv()
token = os.getenv('TOKEN')

client = commands.Bot(command_prefix = ".")

started = False

catparts = {1: {"name": "Body", "value": Image.open("parts/Body1.png")}, 2: {"name": "Ear", "value": Image.open("parts/Ear1.png")}, 3: {"name":"Face", "value": Image.open("parts/Face1.png")}, 4: {"name":"Feet", "value": Image.open("parts/Feet1.png")}, 5:{"name":"Head", "value": Image.open("parts/Head1.png")}, 6:{"name":"Neck", "value": Image.open("parts/Neck1.png")}, 7:{"name":"Tail", "value": Image.open("parts/Tail1.png")}}

pixdata = {}

async def get_bank_data():
  with open("data/bank.json", "r") as f:
    users = json.load(f)
  return users

async def open_account(user):
  users = await get_bank_data()

  #user must already be in number form! DO NOT PASS IN A USERNAME.
  if str(user) in users:
    return
  else:
    users[str(user)] = 100

  with open("data/bank.json", "w") as f:
    json.dump(users,f)
  return

async def start_collection(user):

  if os.path.exists(f"collections/{user}.json"):
    return
  else:
    with open(f"collections/{user}.json", "w") as f:
      json.dump(f)

async def open_collection(user):

  await start_collection(user)
  with open(f"collections/{user}.json", "r") as f:
    collection = json.load(f)

async def update_bank(user, change):
  users = await get_bank_data()

  users[str(user.id)] += change

  with open("data/bank.json", "w") as f:
    json.dump(users, f)

  bal = users[str(user.id)]
  return bal

for x in catparts:
  catvalue = catparts[x]
  catvalue["value"]= catvalue["value"].convert("RGBA")
  pixdata[x] = catvalue["value"].load()

class cat:

  def __init__(self, body, ear, face, feet, head, neck, tail, name, profession):

    for x in catparts:
      self.catparts[x] = {"label" : x, "value": ""}

    self.name = ""
    self.profession = ""

async def create_cat(ctx):

  id = ctx.message.id
  part = {}
  colorpart = {}
  catdict = {}
  for x in catparts:

    catcolorpart = catparts[x]

    img = catcolorpart["value"]
    img = img.convert("RGBA")

    colorr = random.randint(0, 255)
    colorg = random.randint(0, 255)
    colorb = random.randint(0, 255)

    data=np.array(img)  # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    white_areas = (red == 255) & (blue == 255) & (green == 255)
    data[..., :-1][white_areas.T] = (colorr, colorg, colorb)  # Transpose back needed

    im2 = Image.fromarray(data)
    im2.save(f"cats/{id}colorpart{x}.png")

    if x == 1:
      colorpart[x] = Image.open(f"cats/{id}colorpart{x}.png")
      colorpart[x].save(f"cats/{id}part1.png")
    else:
      colorpart[x] = Image.open(f"cats/{id}colorpart{x}.png")
      catvalue1 = colorpart[x]
      part[x] = Image.alpha_composite(catvalue1, Image.open(f"cats/{id}part{x-1}.png"))
      part[x].save(f"cats/{id}part{x}.png")
      part[x].save(f"cats/{id}newcat.png")

    catdict[x] = f"{id}cats/part{x}.png"
    with open(f"cats/{id}cats.json", "w") as f:
      json.dump(catdict, f)

  catdict[8] = f"cats/{id}newcat.png"
  with open(f"cats/{id}cats.json", "w") as f:
    json.dump(catdict, f)
  with open(f'cats/{id}newcat.png', 'rb') as f:
    picture = discord.File(f)
  await ctx.send(file= picture)

  #naming the kitty kitty
  with open("first-names.json", "r") as f:
    firstnames = json.load(f)
  with open("last-names.json", "r") as f:
    lastnames = json.load(f)
  firstnamespin = random.randint(0, len(firstnames))
  lastnamespin = random.randint(0, len(lastnames))

  firstnameentry = firstnames[firstnamespin]
  firstnamefinal = firstnameentry["name"]

  await start_collection(ctx.author.id)
  await ctx.send(f"This kitty's name is {firstnamefinal} {lastnames[lastnamespin]}!")
  catdict[9] = f"{firstnames[firstnamespin]} {lastnames[lastnamespin]}"
  with open(f"collections/{ctx.author.id}.json", "w") as f:
    json.dump(catdict, f)



@client.event
async def on_ready():
  print("Ready")

# Make sure you remove this one!!
@client.command()
async def test(ctx):

  await create_cat(ctx)


@client.command()
async def balance(ctx):

  await open_account(ctx.author.id)
  with open("data/bank.json", "r") as f:
    users = json.load(f)
  string = str(ctx.author.id)
  id = users[string]
  await ctx.send(f"You have {id} kittycoin!")


@client.command()
async def start(ctx):

  global started
  if started == False:
    started = True
    await ctx.author.send("Welcome to Pixel Cats, an incremental trading card game!".format(ctx.author))
    await ctx.author.send("To start, we've got to get you a cat! To create a new cat, use the command .newcat".format(ctx.author))
    await ctx.author.send("But first, you've got to have some money to get a cat! Here, I'll give you 100 kittycoin to start.".format(ctx.author))
    await open_account(ctx.author)
    await ctx.author.send("There, now go ahead and use the .newcat command! Each cat costs 100 kittycoin. (You can check your bank balance with the .balance commmand.")
    await ctx.author.send("You can look at what commands you can use at any time by typing .info.")
    await ctx.author.send("Have fun!")
  else:
    await ctx.author.send("Would you like to restart the game? This action is irreversible. If you would like to do so, simply type .restart, then type .start.")

@client.command()
async def info(ctx):

  await ctx.author.send("Here's a list of the commands available to use in PixelCats."
                        "\n .start: starts/restarts the game."
                        "\n .newcat: creates a new cat (you must have enough kittycoin in your account! Each cat costs 100 kittycoin."
                        "\n .balance: gives you your bank balance in kittycoins.")
@client.command()
async def collection(ctx):

  await ctx.author.send(f"Here's your current kitty collection! You have FILL THIS OUT cats.")



@client.command()
async def restart(ctx):
  global started
  started = False
  with open("data/bank.json", "r") as f:
    users = json.load(f)
  string = str(ctx.author.id)
  del users[string]
  with open("data/bank.json", "w") as f:
    json.dump(users, f)

@client.command()
async def newcat(ctx):

  users = await get_bank_data()
  id = str(ctx.author.id)
  await open_account(id)

  if users[id] < 100:
    await ctx.send("You don't have enough money to get a new cat! Come back when you have more kittycoin.")
  else:
    await create_cat(ctx)
    await update_bank(ctx.author, -100)


client.run(token)