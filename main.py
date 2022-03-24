import os
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import Client, Intents, Embed
import json


def get_prefix(client, message):
  with open('prefixes.json','r') as f:
    prefix = json.load(f)
  arr=[]
  arr.append(prefix[str(message.guild.id)])
  x= str(client.user.mention) + " " 
  y= str(client.user.mention)[:2] + "!" + str(client.user.mention)[2:] + " "
  arr.append(x)
  arr.append(y)
  return arr

def server_prefix(ctx):
  with open('prefixes.json','r') as f:
    prefixes = json.load(f)

  return prefixes[str(ctx.guild.id)]

my_secret = os.environ['token']
intents = discord.Intents.all()
client = commands.Bot (command_prefix = get_prefix,intents=intents, help_command=None)


fileObj = open("yukiplaylist", "r")
words = fileObj.read().splitlines() 
fileObj.close()

fileObj = open("hachiplaylist", "r")
words2 = fileObj.read().splitlines() 
fileObj.close()

def check_owner(ctx):
  if (ctx.author.id==620402532346232832 or ctx.author.id==800531315602227241 or ctx.author.id==555494011947974667):
    return True

@client.event
async def on_guild_join(guild):
  with open ("prefixes.json",'r') as f:
    prefixes = json.load(f)

  prefixes[str(guild.id)]='='
  
  with open ("prefixes.json",'w') as f:
      json.dump(prefixes,f,indent=4)

  with open ("q.json",'r') as f:
    q = json.load(f)

  q[str(guild.id)]=[]
  
  with open ("q.json",'w') as f:
      json.dump(q,f,indent=4)

  embed=discord.Embed(title="How to use Meloetta", description="Discord Music Bot", color=1752220)
  embed.set_author(name="Meloetta",icon_url=client.user.avatar_url)
  embed.set_thumbnail(url=guild.icon_url)
  embed.add_field(name="`=p [song name | youtube url]`",value="*Plays a song when given the name of the song and artist (optional) or youtube URL*\n", inline=False)
  retval=""
  embed.add_field(name="`=q`",value="*Displays the whole queue of songs*\n", inline=False)
  embed.add_field(name="`=np`",value="*Displays the name of the song currently playing*\n", inline=False)
  embed.add_field(name="`=skip`",value="*Skips the currently playing song*\n", inline=False)
  #embed.add_field(name="`+remove`",value="*Removes a song from the queue (give the song's queue number)*\n", inline=False)
  #embed.add_field(name="`+select`",value="*Skips directly to a song in the queue (give the song's queue number)*\n", inline=False)
  embed.add_field(name="`=mix`",value="*Shuffles the queue of songs*\n", inline=False)
  embed.add_field(name="`=clear`",value="*Empties the whole queue of songs*\n", inline=False)
  
  #embed.add_field(name="`+playlist`",value="*Loads your playlist into the queue (give your name), but only works if you have submitted a queue to the short, stupid jerk*\n", inline=False)
  embed.add_field(name="`=ping`",value="*Displays the ping of the bot*\n", inline=False)
  embed.add_field(name="`=dc`",value="*Disconnects the bot from the voice channel*\n", inline=False)
  embed.add_field(name="`=setprefix [new prefix]`",value="*Changes prefix when given a new prefix*\n", inline=False)
  embed.add_field(name="`=prefix`",value="*Displays prefix of this server*\n", inline=False)
  embed.set_footer(text="Thanks for using Meloetta ^-^")
  for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(embed=embed)
        break
    
@client.command()
@commands.has_permissions(manage_channels=True)
async def setprefix(ctx,new_prefix):
  with open('prefixes.json','r') as f:
      prefixes=json.load(f)
    
  prefixes[str(ctx.guild.id)] = new_prefix

  with open ("prefixes.json",'w') as f:
      json.dump(prefixes,f,indent=4)
    
  print(prefixes[str(ctx.guild.id)])
  await ctx.send(f"```Prefix changed to {new_prefix}```")

@client.command()
async def prefix(ctx):
  x = server_prefix(ctx)
  await ctx.send(f"```Current Prefix for Meloetta: {x}```")

@setprefix.error
async def setprefix_error(ctx, error):
  if isinstance(error,commands.MissingRequiredArgument):
    await ctx.send("```Please include the prefix you would like to set as your server's prefix for Meloetta.```")
    
@client.command()
@commands.check(check_owner)
async def reload(ctx, *, extension):
  client.unload_extension(f'cogs.{extension}')
  client.load_extension(f'cogs.{extension}')
  await ctx.send(f"```Succesfully Reloaded {extension}```")

@client.command()
@commands.check(check_owner)
async def unload(ctx, *, extension):
  client.unload_extension(f'cogs.{extension}')
  await ctx.send(f"```Succesfully Unloaded {extension}```")

@client.command()
@commands.check(check_owner)
async def load(ctx, *, extension):
  client.load_extension(f'cogs.{extension}')
  await ctx.send(f"```Succesfully Loaded {extension}```")

for filename in os.listdir('MusicBot/cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

#bot active
@client.event
async def on_ready(): 
  await client.change_presence(status=discord.Status.dnd, activity=discord.Game("music - inv link in bio"))
  print('Bot is Ready.')

@client.command()
async def help(ctx):
  x = server_prefix(ctx)
  embed=discord.Embed(title="How to use Meloetta", description="Discord Music Bot", color=1752220)      
  embed.set_author(name="Meloetta",icon_url=client.user.avatar_url)
  embed.set_thumbnail(url=ctx.guild.icon_url)
  embed.add_field(name=f"`{x}p [song name | youtube url]`",value="*Provide name of the song and artist (for better result) or youtube URL*\n", inline=False)
  retval=""
  embed.add_field(name=f"`{x}q`",value="*Displays the whole queue of songs*\n", inline=False)
  embed.add_field(name=f"`{x}np`",value="*Displays the name of the song currently playing*\n", inline=False)
  embed.add_field(name=f"`{x}skip`",value="*Skips the currently playing song*\n", inline=False)
  #embed.add_field(name="`+remove`",value="*Removes a song from the queue (give the song's queue number)*\n", inline=False)
  #embed.add_field(name="`+select`",value="*Skips directly to a song in the queue (give the song's queue number)*\n", inline=False)
  embed.add_field(name=f"`{x}mix`",value="*Shuffles the queue of songs*\n", inline=False)
  embed.add_field(name=f"`{x}clear`",value="*Empties the whole queue of songs*\n", inline=False)
  
  #embed.add_field(name="`+playlist`",value="*Loads your playlist into the queue (give your name), but only works if you have submitted a queue to the short, stupid jerk*\n", inline=False)
  embed.add_field(name=f"`{x}ping`",value="*Displays the ping of the bot*\n", inline=False)
  embed.add_field(name=f"`{x}dc`",value="*Disconnects the bot from the voice channel*\n", inline=False)
  embed.add_field(name=f"`{x}setprefix [new prefix]`",value="*Changes prefix when given a new prefix*\n", inline=False)
  embed.add_field(name=f"`{x}prefix`",value="*Displays prefix of this server*\n", inline=False)
  embed.set_footer(text="Thanks for using Meloetta ^-^")
  await ctx.send(embed=embed)
    
client.run(my_secret)