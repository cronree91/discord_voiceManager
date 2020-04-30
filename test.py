# インストールした discord.py を読み込む
import discord
import sys, os

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'Njk5NTk5MDcxMTE1MjE0OTA5.Xpaddg.Znv75oYZ4Zuc7UDmNjTnzZuCs4g'

# 接続に必要なオブジェクトを生成
client = discord.Client()

@client.event
async def on_message(message):
    if message.author.bot:
        return
    elif message.content == "sys/debug":
        await message.channel.send(message.author.status)

client.run(TOKEN)
