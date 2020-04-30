# インストールした discord.py を読み込む
import discord
import sys, os

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'Njk5NTk5MDcxMTE1MjE0OTA5.XpcDRw._dDGc3_h1Cf7RG8adRDkBJ3npuY'

LOG_CH = 696649704867364885
ADMIN_ROLE = 697241231595536385
# 接続に必要なオブジェクトを生成
client = discord.Client()

channels = []

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    channel = client.get_channel(LOG_CH)
    await channel.send("ログインしました。")

@client.event
async def on_disconnect():
    # 起動したらターミナルにログイン通知が表示される
    print('ログアウトしました')
    channel = client.get_channel(LOG_CH)
    await channel.send("ログアウトしました。")


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    elif message.content == "sys/debug":
        await message.channel.send(message.author.name)
        await message.channel.send(message.author.top_role.name+"("+str(message.author.top_role.id)+")")
        await message.channel.send(message.author.roles)
    elif message.author.top_role.id == ADMIN_ROLE:
        if message.content.startswith('vc/create'):
            ch = await message.guild.categories[list(map(lambda x: x.name, message.guild.categories)).index("ボイスチャンネル")].create_voice_channel("➕ 新規作成["+message.content[10:]+"]")
            channels.append(ch)
            await message.channel.send("作成しました。")
        elif message.content.startswith('sys/exit'):
            exit(0)

@client.event
async def on_voice_state_update(member, before, after):
    channel = client.get_channel(LOG_CH)
    if before.channel==None:
        if after.channel in channels:
            ch = await after.channel.guild.categories[list(map(lambda x: x.name, after.channel.guild.categories)).index("ボイスチャンネル")].create_voice_channel(after.channel.name[6:])
            await member.move_to(ch)
        else:
            await channel.send(str(member)+"が"+str(after.channel)+"へ参加しました。")
    elif after.channel==None:
        await channel.send(str(member)+"が"+str(before.channel)+"から脱退しました。")
        if before.channel.members == []:
            await channel.send(before.channel.name+"の参加者数が0人になったため、削除します。")
            await before.channel.delete()


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
