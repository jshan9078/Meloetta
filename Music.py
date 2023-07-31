import discord
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import has_permissions
from youtube_dl import YoutubeDL
from main import words, words2
import requests
import random
import json

class Music(commands.Cog):

  def __init__(self, client):
    self.client = client

    self.is_playing=False
    #self.music_queue=[]
    self.music_queue={}
    self.now_playing={}
    #self.request_queue=[]
    #self.now_playing="No song is playing."
    self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    self.vc = {}
    
    with open ("prefixes.json",'r') as f:
      servers = json.load(f)

    for key in servers:
      self.music_queue[str(key)]=[]
      self.vc[str(key)]=""
      self.now_playing[str(key)]="Not currently playing anything :("
  
  def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}
          
  def play_next(self, ctx):
      if len(self.music_queue[str(ctx.guild.id)]) > 0:
          self.is_playing = True

          #get the first url
          m_url = self.music_queue[str(ctx.guild.id)][0][0]['source']
         
          self.now_playing[str(ctx.guild.id)]=str(self.music_queue[str(ctx.guild.id)][0][0]['title'])

          #remove the first element as you are currently playing it
          self.music_queue[str(ctx.guild.id)].pop(0)
          #self.request_queue.pop(0)

         
          self.vc[str(ctx.guild.id)].play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
      else:
        if self.is_playing==False:
          self.now_playing[str(ctx.guild.id)]="Not currently playing anything :("
        self.is_playing = False
          
         

  
  @commands.command()
  async def np(self,ctx):
    await ctx.send(f"**{str(self.now_playing[str(ctx.guild.id)])}**")
  
  
  async def play_music(self,ctx):
      if len(self.music_queue[str(ctx.guild.id)]) > 0:
          self.is_playing = True
          
          m_url = self.music_queue[str(ctx.guild.id)][0][0]['source']
          self.now_playing[str(ctx.guild.id)]=str(self.music_queue[str(ctx.guild.id)][0][0]['title'])
          
          
          if self.vc[str(ctx.guild.id)] == "" or not self.vc[str(ctx.guild.id)].is_connected() or self.vc == None:
              self.vc[str(ctx.guild.id)] = await self.music_queue[str(ctx.guild.id)][0][1].connect()
              
          else:
              await self.vc[str(ctx.guild.id)].move_to(self.music_queue[str(ctx.guild.id)][0][1])
          
          

          self.vc[str(ctx.guild.id)].play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
        
          if len(self.music_queue[str(ctx.guild.id)])==1:
             self.music_queue[str(ctx.guild.id)].pop(0)
            
      else:
          self.is_playing = False
          #self.now_playing[str(ctx.guild.id)]="Not currently playing anything :("
          

  @commands.command()
  async def p(self, ctx, *args):
      query = " ".join(args)
      if ctx.author.voice is None:
          await ctx.send("Connect to a voice channel!")
      else:
          user = ctx.message.author
          vc = user.voice.channel
          voice_channel = ctx.author.voice.channel
          song = self.search_yt(query)
          if (song==False):
              await ctx.send("API error :(\n Please try another song")
          elif type(song) == type(True):
              await ctx.send("Please enter a valid song.")
          else:
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice == None:
              #self.request_queue.append(query)
              await ctx.send(f"Joined **{vc}**")
              self.music_queue[str(ctx.guild.id)].append([song, voice_channel])
              await self.play_music(ctx)
              #self.now_playing[str(ctx.guild.id)]=str(self.music_queue[0][0]['title'])
              self.music_queue[str(ctx.guild.id)].pop(0)
              #self.request_queue.pop(0)
            elif len(self.music_queue[str(ctx.guild.id)])==0:
              await ctx.send("Song added to the queue")
              self.music_queue[str(ctx.guild.id)].append([song, voice_channel])
              #self.request_queue.append(query)
              await self.play_music(ctx)
              self.music_queue[str(ctx.guild.id)].pop(0)
              #self.request_queue.pop(0)
            elif voice!=None:
              await ctx.send("Song added to the queue")
              self.music_queue[str(ctx.guild.id)].append([song, voice_channel])
              #self.music_queue.append([song, voice_channel])
              #self.request_queue.append(query)


  
  @commands.command()
  async def clear(self,ctx):
    self.music_queue[str(ctx.guild.id)]=[]
    #self.request_queue=[]
    await ctx.send("Cleared queue")
  

  @commands.command(name="skip")
  async def skip(self, ctx):
      if self.vc[str(ctx.guild.id)]  != "" and self.vc[str(ctx.guild.id)] :
          self.vc[str(ctx.guild.id)] .stop()
          await self.play_music(ctx)

  @commands.command()
  async def mix(self,ctx):
    random.shuffle(self.music_queue[str(ctx.guild.id)])
    await ctx.send("Queue has been shuffled.")
        
  
  @commands.command()
  async def q(self, ctx):
      retval = ""
      retval2 = ""
      for i in range(0, len(self.music_queue[str(ctx.guild.id)])):
          retval += f"**{i+1}**" + " " + f"`{str(self.music_queue[str(ctx.guild.id)][i][0]['title'])}`" + "\n"
          retval2 += str(self.music_queue[str(ctx.guild.id)][i][0]) + "\n"

      if retval != "":
          await ctx.send(retval)
          
      else:
          await ctx.send("No music in queue")
  

  #ping command
  @commands.command()
  async def ping(self, ctx):
    await ctx.send(f'```Current Ping: {round(self.client.latency*1000)} ms```')

  
  @commands.command()
  async def dc(self, ctx):
    song = self.search_yt("Stay alive -  Jungkook")
    voice_channel = ctx.author.voice.channel
    self.music_queue[str(ctx.guild.id)].insert(0,[song, voice_channel])
    for x in self.client.voice_clients:
        if(x.guild.id == ctx.message.guild.id):
            await ctx.send("Disconnecting Now")
            return await x.disconnect()
    

  
def setup(client):
  client.add_cog(Music(client))
