import discord
import sys, os
import ast
import time
from datetime import datetime
TOKEN = 'Njk5OTY3NzM1NTM4Mzg0OTg3.XpcFyQ.e7_bFu3pi2qXbo9gDyD5TkHGBZI'
groups = {699887698369970266: {}}

client = discord.Client()
channels = []

def logs(msg):
    print("["+str(time.time())+"]"+msg)

@client.event
async def on_ready():
    print(groups)
    logs("Bot is ready!")

@client.event
async def on_connect():
    logs("The bot has logged in.")

@client.event
async def on_disconnect():
    logs("The bot has been logged out.")

@client.event
async def on_guild_join(guild):
    groups[guild.id] = {}
    embed = discord.Embed(title="Hi!",description="I'm a server management bot!\nAnd if you don't know how to use it, just say '/help`!",color=discord.Colour.red())
    await guild.system_channel.send(embed=embed)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    elif message.content == "/help":
        embed = discord.Embed(title="Help",description="")
        embed.add_field(name="Debug Command",value="`debug/profile` Show your profile.\n`debug/info` Show your server's profile.",inline=False)
        embed.add_field(name="Voice Chat Command",value="`vc/create` Create new voice channel",inline=False)
        embed.add_field(name="Setting Command",value="`set/creater_role` Set your server's creater's role.\n`set/vc_categories` Set vc's categorie.",inline=False)
        embed.add_field(name="Manage Command",value="`mng/ban <Mention>` Ban\n`mng/kick <Mention>` Kick.\n`mng/unban <Mention>` Unban.\n`mng/bans` Show listed bans.",inline=False)
        embed.add_field(name="System Command ( Only use cronちゃん )",value="`sys/save`\n`sys/load`",inline=False)
        await message.channel.send(embed=embed)
    elif message.content == "sys/load":
        if message.author != client.get_user(431707293692985344):
            await message.channel.send("This command only use cronちゃん.")
            return(0)
        with open("save.txt") as f:
            s = f.read()
            groups = ast.literal_eval(s)
        await message.channel.send("Loaded")
    elif message.content == "sys/save":
        if message.author != client.get_user(431707293692985344):
            await message.channel.send("This command only use cronちゃん.")
            return(0)
        with open("save.txt", "w") as f:
            f.write(str(groups))
        await message.channel.send("Saved")
    elif message.content.startswith("mng/kick"):
        if 'creater_role' not in groups[message.guild.id]:
            await message.channel.send("Please set creater's role!")
            return(0)
        guild = message.guild
        if guild.get_role(groups[guild.id]['creater_role']) in message.author.roles:
            pass
        else:
            await message.channel.send("It's only creater's command!")
            return(0)
        await message.guild.kick(client.get_user(message.raw_mentions[0]))
    elif message.content.startswith("mng/bans"):
        guild = message.guild
        bans = guild.bans
        await message.channel.send(map(lambda x: x.name, bans.user).join("\n"))
    elif message.content.startswith("mng/unban"):
        if 'creater_role' not in groups[message.guild.id]:
            await message.channel.send("Please set creater's role!")
            return(0)
        guild = message.guild
        if guild.get_role(groups[guild.id]['creater_role']) in message.author.roles:
            pass
        else:
            await message.channel.send("It's only creater's command!")
            return(0)
        await message.guild.unban(client.get_user(message.raw_mentions[0]))
    elif message.content.startswith("mng/ban"):
        if 'creater_role' not in groups[message.guild.id]:
            await message.channel.send("Please set creater's role!")
            return(0)
        guild = message.guild
        if guild.get_role(groups[guild.id]['creater_role']) in message.author.roles:
            pass
        else:
            await message.channel.send("It's only creater's command!")
            return(0)
        await message.guild.ban(client.get_user(message.raw_mentions[0]))
    elif message.content == "debug/profile":
        user = message.author
        embed = discord.Embed(title=(user.name+"#"+user.discriminator), description=str(user.id))
        embed.add_field(name="JOINED_AT",value=user.joined_at.strftime("%Y/%m/%d"),inline=False)
        embed.add_field(name="NickName",value=user.nick,inline=False)
        embed.add_field(name="Status",value=user.status,inline=False)
        embed.add_field(name="Roles",value="\n".join(map(lambda x: x.name+":"+str(x.id),user.roles)),inline=False)
        embed.add_field(name="Top Role",value=user.top_role.name+":"+str(user.top_role.id),inline=False)
        embed.add_field(name="Display Name", value=user.display_name,inline=False)
        embed.add_field(name="Activity", value=user.activity,inline=False)
        embed.set_thumbnail(url=str(user.avatar_url))
        await message.channel.send(embed=embed)
    elif message.content == "debug/info":
        guild = message.guild
        embed = discord.Embed(title=guild.name+":"+str(guild.id), description=guild.description)
        embed.add_field(name="Emojis", value=guild.emojis,inline=False)
        embed.add_field(name="Region", value=guild.region,inline=False)
        embed.add_field(name="AFK", value="TimeOut: "+str(guild.afk_timeout)+"\nChannel:"+str(guild.afk_channel),inline=False)
        embed.add_field(name="Icon", value=guild.icon,inline=False)
        embed.add_field(name="Owner", value=client.get_user(guild.owner_id).name+"#"+client.get_user(guild.owner_id).discriminator+":"+str(guild.owner_id),inline=False)
        embed.add_field(name="Created",value="at "+guild.created_at.strftime("%Y/%m/%d"),inline=False)
        embed.set_thumbnail(url=str(guild.banner_url))
        await message.channel.send(embed=embed)

    elif message.content == "set/creater_role":
        guild = message.guild
        print(groups)
        if 'creater_role' in groups[guild.id]:
            if guild.get_role(groups[guild.id]['creater_role']) in message.author.roles:
                pass
            else:
                await message.channel.send("It is already registered.")
                return(0)
        guild = message.guild
        roles = {}
        stri = ""
        i = 1
        for x in guild.roles[::-1]:
            stri = stri+str(i)+". "+x.name+"\n"
            roles[i] = x.id
            i+=1
        print(roles)
        embed = discord.Embed(title="Roles", description=stri)
        await message.channel.send(embed=embed)
        def check(m):
            return m.author == message.author and m.channel == message.channel
        try:
            m = await client.wait_for("message",timeout=60.0,check=check)
        except asyncio.TimeoutError:
            await message.channel.send("Time outed!")
        else:
            if int(m.content) in roles:
                groups[guild.id]['creater_role'] = roles[int(m.content)]
                await message.channel.send(guild.get_role(roles[int(m.content)]).name+" has been registered as the role of creator.")
            else:
                await message.channel.send("Unknown reaction!")
    elif message.content.startswith('set/vc_categories'):
        if 'creater_role' not in groups[message.guild.id]:
            await message.channel.send("Please set creater's role!")
            return(0)
        guild = message.guild
        if guild.get_role(groups[guild.id]['creater_role']) in message.author.roles:
            pass
        else:
            await message.channel.send("It's only creater's command!")
            return(0)
        groups[message.guild.id]['vc_categories'] = message.content[18:]
        await message.channel.send("I set "+message.content[18:]+" to the voice chat category.")
    elif message.content.startswith('vc/create'):
        if 'creater_role' not in groups[message.guild.id]:
            await message.channel.send("Please set creater's role!")
            return(0)
        guild = message.guild
        if guild.get_role(groups[guild.id]['creater_role']) in message.author.roles:
            pass
        else:
            await message.channel.send("It's only creater's command!")
            return(0)
        ch = await guild.categories[list(map(lambda x: x.name, guild.categories)).index(groups[guild.id]['vc_categories'])].create_voice_channel("➕ 新規作成["+message.content[10:]+"]")
        if 'vc_channels' in groups[message.guild.id]:
            groups[message.guild.id]['vc_channels'][ch.id] = message.content[10:]
            groups[message.guild.id]['vc_channels_count'][ch.id] = 0
        else:
            groups[message.guild.id]['vc_channels'] = {}
            groups[message.guild.id]['vc_channels_count'] = {}
            groups[message.guild.id]['vc_top_channels'] = {}
            groups[message.guild.id]['vc_channels'][ch.id] = message.content[10:]
            groups[message.guild.id]['vc_channels_count'][message.content[10:]] = 0
        await message.channel.send("Created")

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel==None:
        guild = after.channel.guild
        if after.channel.id in groups[guild.id]['vc_channels']:
            groups[guild.id]['vc_channels_count'][groups[guild.id]['vc_channels'][after.channel.id]] += 1
            ch = await guild.categories[list(map(lambda x: x.name, after.channel.guild.categories)).index(groups[guild.id]['vc_categories'])].create_voice_channel("["+groups[guild.id]['vc_channels'][after.channel.id]+"]  "+str(groups[guild.id]['vc_channels_count'][groups[guild.id]['vc_channels'][after.channel.id]]))
            groups[guild.id]['vc_top_channels'][ch.id] = groups[guild.id]['vc_channels'][after.channel.id]
            await member.move_to(ch)
        else:
            await guild.system_channel.send(str(member)+" is joined to "+str(after.channel))
    elif after.channel==None:
        guild = before.channel.guild
        await guild.system_channel.send(str(member)+" left from "+str(before.channel))
        if before.channel.members == []:
            print(groups[guild.id]['vc_channels'])
            print(before.channel.id)
            if before.channel.id in groups[guild.id]['vc_top_channels']:
                await guild.system_channel.send(before.channel.name+" is deleted because the number of "+before.channel.name+"s is now 0.")
                groups[guild.id]['vc_channels_count'][groups[guild.id]['vc_top_channels'][before.channel.id]] -= 1
                await before.channel.delete()


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
