import discord
import sys, os
import ast
import time
import asyncio
from datetime import datetime
TOKEN = "Njk5OTY3NzM1NTM4Mzg0OTg3.Xp5-8g.oep2ZHiem0JYI8aB1gwUWL3Ghww"

groups = {699887698369970266: {}}

client = discord.Client()

async def logs(msg, guild=None,cmd_msg=True):
  if guild is None:
    print('[{0}]{1}'.format(time.time(), msg))
  else:
    if cmd_msg:
      print('[{0}][{1}:{2}]{3}'.format(time.time(), guild.name, guild.id, msg))
    if guild.system_channel is None:
      pass
    else:
      await guild.system_channel.send('[{0}]{1}'.format(str(time.time()), msg))

# def error(msg, guild=None):
#   if guild is None:
#     print('ERROR[{0}]{1}'.format(time.time(), msg))
#   else:
#     print('ERROR[{0}][{1}:{2}]{3}'.format(time.time(), guild.name, guild.id, msg))
#     guild.system_channel.send('ERROR[{0}]{1}'.format(time.time(), guild.name, guild.id, msg))

@client.event
async def on_ready():
  for x in client.guilds:
    await logs("Bot is ready!",x,False)
  await logs("Bot is ready!")

@client.event
async def on_connect():
  for x in client.guilds:
    await logs("Bot has logged in!",x,False)
  await logs("Bot has logged in!")

@client.event
async def on_disconnect():
  for x in client.guilds:
    await logs("Bot has been logged out!",x,False)
  await logs("Bot has been logged out!")


@client.event
async def on_guild_join(guild):
    groups[guild.id] = {}
    embed = discord.Embed(title="Hi!",description="I'm a server management bot!\nAnd if you don't know how to use it, just say '/help`!",color=discord.Colour.red())
    await guild.system_channel.send(embed=embed)

@client.event
async def on_message(msg):
  if msg.author.bot:
    return
  elif msg.content == "/help":
    await helps(msg)
  # elif msg.content.startswith("sys/"):
  #   pass
  elif msg.content.startswith("debug/"):
    await debug(msg)
  elif msg.content.startswith("vc/"):
    await vcmng(msg)
  elif msg.content.startswith("set/"):
    await setting(msg)
  elif msg.content.startswith("mng/"):
    await mng(msg)

async def mng(msg):
  # if msg.content.startswith("mng/unban"):
  #   guild = msg.guild
  #   if 'creater_role' not in groups[guild.id]:
  #     await msg.channel.send("Please set creater's role!")
  #     return(0)
  #   if guild.get_role(groups[guild.id]['creater_role']) in msg.author.roles:
  #     pass
  #   else:
  #     await msg.channel.send("It's only creater's command!")
  #     return(0)
  #   await msg.guild.unban(client.get_user(msg.raw_mentions[0]))
  # elif msg.content.startswith("mng/bans"):
  #   guild = msg.guild
  #   bans = guild.bans
  #   # await msg.channel.send()
  #   print(list(bans))
  #   # list(map(lambda x: ('{0}:{1}'.format(x.name,x.id)),bans)).join("\n")
  if msg.content.startswith("mng/ban"):
    guild = msg.guild
    if 'creater_role' not in groups[msg.guild.id]:
      await msg.channel.send("Please set creater's role!")
      return(0)
    if guild.get_role(groups[guild.id]['creater_role']) in msg.author.roles:
      pass
    else:
      await msg.channel.send("It's only creater's command!")
      return(0)
    await msg.guild.ban(client.get_user(msg.raw_mentions[0]))
  elif msg.content.startswith("mng/kick"):
    guild = msg.guild
    if 'creater_role' not in groups[msg.guild.id]:
      await msg.channel.send("Please set creater's role!")
      return(0)
    if guild.get_role(groups[guild.id]['creater_role']) in msg.author.roles:
      pass
    else:
      await msg.channel.send("It's only creater's command!")
      return(0)
    await msg.guild.kick(client.get_user(msg.raw_mentions[0]))
  else:
    await msg.channel.send("Unknown mng command!")

@client.event
async def on_voice_state_update(member, before, after):
  if before.channel==None: # ボイチャへの加入
    guild = after.channel.guild
    await guild.system_channel.send('{0} joined to {1}'.format(member, before.channel))
    if after.channel.id in groups[guild.id]['vc_ch']:
      if groups[guild.id]['vc_ch'][after.channel.id]['kind']=='ROOT':
        ch = await guild.categories[list(map(lambda x: x.name, after.channel.guild.categories)).index(groups[guild.id]['vc_categories'])].create_voice_channel('No.{0} [{1}]'.format(len(groups[guild.id]['vc_ch'][after.channel.id]['leafs'])+1, groups[guild.id]['vc_ch'][after.channel.id]['name']))
        ch_text = await guild.categories[list(map(lambda x: x.name, after.channel.guild.categories)).index(groups[guild.id]['vc_categories'])].create_text_channel('{1}_{0}'.format(len(groups[guild.id]['vc_ch'][after.channel.id]['leafs'])+1, groups[guild.id]['vc_ch'][after.channel.id]['name']))

        groups[guild.id]['vc_ch'][ch.id] = {'kind': 'LEAF','name': groups[guild.id]['vc_ch'][after.channel.id]['name'], 'leafs': None,'root': after.channel.id,'text':ch_text.id}
        groups[guild.id]['vc_ch'][after.channel.id]['leafs'].append(ch.id)
        await member.move_to(ch)
  elif after.channel==None: # ボイチャからの離脱
    guild = before.channel.guild
    await guild.system_channel.send('{0} left from {1}'.format(member, before.channel))
    if before.channel.members == []:
      if before.channel.id in groups[guild.id]['vc_ch']:
        if groups[guild.id]['vc_ch'][before.channel.id]['kind'] == 'LEAF':
          await guild.system_channel.send('{0} is deleted because the number of {0}s is now 0.'.format(before.channel.name))
          v = groups[guild.id]['vc_ch'].pop(before.channel.id)
          groups[guild.id]['vc_ch'][v['root']]['leafs'].remove(before.channel.id)
          await before.channel.delete()
          await client.get_channel(v['text']).delete()

""" MEMO

{
  "GROUP_ID": {
    'vc_ch': {
      'CH_ID': {
        'kind': 'ROOT_OR_LEAF',
        'name': 'NAME',
        'leafs': [LEAFS]|NONE,
        'root': 'ROOT_ID'|NONE,
        'text': 'TEXT_CHANNEL_ID'
      }
    }
  }
}

"""

async def vcmng(msg):
  if msg.content.startswith('vc/create'):
    if 'creater_role' not in groups[msg.guild.id]:
        await msg.channel.send("Please set creater's role!")
        return(0)
    guild = msg.guild
    if guild.get_role(groups[guild.id]['creater_role']) in msg.author.roles:
        pass
    else:
        await msg.channel.send("It's only creater's command!")
        return(0)
    ch = await guild.categories[list(map(lambda x: x.name, guild.categories)).index(groups[guild.id]['vc_categories'])].create_voice_channel("➕ 新規作成["+msg.content[10:]+"]")
    if 'vc_ch' in groups[msg.guild.id]:
        groups[msg.guild.id]['vc_ch'][ch.id] = {'kind': 'ROOT','name': msg.content[10:],'leafs': [],'root': None}
    else:
        groups[msg.guild.id]['vc_ch'] = {}
        groups[msg.guild.id]['vc_ch'][ch.id] = {'kind': 'ROOT','name': msg.content[10:],'leafs': [],'root': None}
    await msg.channel.send("Created!")
  else:
    await msg.channel.send("Unknown vc command!")


async def debug(msg):
  if msg.content.startswith("debug/profile"):
    user = msg.author
    embed = discord.Embed(title=(user.name+"#"+user.discriminator), description=str(user.id))
    embed.add_field(name="JOINED_AT",value=user.joined_at.strftime("%Y/%m/%d"),inline=False)
    embed.add_field(name="NickName",value=user.nick,inline=False)
    embed.add_field(name="Status",value=user.status,inline=False)
    embed.add_field(name="Roles",value="\n".join(map(lambda x: x.name+":"+str(x.id),user.roles)),inline=False)
    embed.add_field(name="Top Role",value=user.top_role.name+":"+str(user.top_role.id),inline=False)
    embed.add_field(name="Display Name", value=user.display_name,inline=False)
    embed.add_field(name="Activity", value=user.activity,inline=False)
    embed.set_thumbnail(url=str(user.avatar_url))
    await msg.channel.send(embed=embed)
  elif msg.content.startswith("debug/info"):
    guild = msg.guild
    embed = discord.Embed(title=guild.name+":"+str(guild.id), description=guild.description)
    embed.add_field(name="Emojis", value=guild.emojis,inline=False)
    embed.add_field(name="Region", value=guild.region,inline=False)
    embed.add_field(name="AFK", value="TimeOut: "+str(guild.afk_timeout)+"\nChannel:"+str(guild.afk_channel),inline=False)
    embed.add_field(name="Icon", value=guild.icon,inline=False)
    embed.add_field(name="Owner", value=client.get_user(guild.owner_id).name+"#"+client.get_user(guild.owner_id).discriminator+":"+str(guild.owner_id),inline=False)
    embed.add_field(name="Created",value="at "+guild.created_at.strftime("%Y/%m/%d"),inline=False)
    embed.set_thumbnail(url=str(guild.banner_url))
    await msg.channel.send(embed=embed)
  else:
    await msg.channel.send("Unkown debug command!")

async def setting(msg):
  if msg.content.startswith("set/creater_role"):
    guild = msg.guild
    if 'creater_role' in groups[guild.id]:
      if guild.get_role(groups[guild.id]['creater_role']) in msg.author.roles:
        pass
      else:
        await msg.channel.send("Creater's role is already registered.")
        return(0)
    roles = {}
    result = ""
    i = 1
    for x in guild.roles[::-1]:
        result = result+'{0}. {1}\n'.format(i,x.name)
        roles[i] = x.id
        i+=1
    embed = discord.Embed(title="Roles", description=result)
    await msg.channel.send(embed=embed)

    def check(m):
      return m.author == msg.author and m.channel == msg.channel

    try:
      m = await client.wait_for("message",timeout=60.0,check=check)
    except asyncio.TimeoutError:
      await msg.channel.send("Time outed!")
    else:
      if int(m.content) in roles:
        groups[guild.id]['creater_role'] = roles[int(m.content)]
        await msg.channel.send(guild.get_role(roles[int(m.content)]).name+" has been registered as the role of creator.")
      else:
        await msg.channel.send("Unknown reaction!")
  elif msg.content.startswith("set/vc_categories"):
    guild = msg.guild
    if 'creater_role' not in groups[msg.guild.id]:
      await msg.channel.send("Please set creater's role!")
      return(0)
    if guild.get_role(groups[guild.id]['creater_role']) in msg.author.roles:
      pass
    else:
      await msg.channel.send("It's only creater's command!")
      return(0)
    groups[msg.guild.id]['vc_categories'] = msg.content[18:]
    await msg.channel.send("I set "+msg.content[18:]+" to the voice chat category.")
  else:
    await msg.channel.send("Unknown set command!")

async def helps(msg):
  embed = discord.Embed(title="Help",description="")
  embed.add_field(name="Debug Command",value=(
    "`debug/profile` Show your profile.\n"
    "`debug/info` Show your server's profile."
    ),inline=False)
  embed.add_field(name="Voice Chat Command",value=(
    "`vc/create` Create new voice channel"
    ),inline=False)
  embed.add_field(name="Setting Command",value=(
    "`set/creater_role` Set your server's creater's role.\n"
    "`set/vc_categories <Categorie Name>` Set vc's categorie."
    ),inline=False)
  embed.add_field(name="Manage Command",value=(
    "`mng/ban <Mention>` Ban\n"
    "`mng/kick <Mention>` Kick.\n"
    "`mng/unban <Mention>` Unban.\n"
    # "`mng/bans` Show listed bans."
    ),inline=False)
  # embed.add_field(name="System Command ( Only use cronちゃん )",value=(
  #   "`sys/save`\n"
  #   "`sys/load`"
  #   ),inline=False)
  await msg.channel.send(embed=embed)

client.run(TOKEN)