#-*- -*- -*- -*- -*- -*- -*- -*- coding:UTF-8 -*- -*- -*- -*- -*- -*- -*- -*- -
import discord
from discord import app_commands
# from discord.ext import commandslash_commands, Option, OptionType
# import random
import os
#-*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*- -*

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])
CHECK_GUILD = int(os.environ["CHECK_GUILD"])


intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.typing = False

# bot = commands.Bot(command_prefix = '.',intents=intents, help_command=None)
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)
# tree = bot.tree
set_guild = discord.Object(CHECK_GUILD)

# スラッシュコマンドを使えるサーバー列挙
notifyGuilds = [CHECK_GUILD]

@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)
    print("discord.py -> " + discord.__version__)  # discord.pyのバージョン
    print('------')
    await bot.change_presence(activity=discord.Game(name="ver2.0.1"))
    await tree.sync()

# 役職を追加する
@tree.command(
    name = 'add_role',
    description = '通知される役職に登録します。'
)
async def add_role(inter):
    role = discord.utils.get(inter.guild.roles, name="notify") # サーバー内の「ロール名」というロールを取得
    member = inter.author
    await member.add_roles(role) # 上記で取得したロールを付与
    await inter.reply('役職を追加しました')

# 役職を削除する
@tree.command(
    name = 'remove_role',
    description = '通知される役職に登録します。'
)
async def remove_role(inter):
    role = discord.utils.get(inter.guild.roles, name="notify")
    await inter.author.remove_roles(role) # 上記で取得したロールを剥奪
    await inter.reply('役職を削除しました')

@bot.event
async def on_voice_state_update(member, before, after):
    print(after.channel)
    print(member)
    print("-------------------")
    if member.guild.id == CHECK_GUILD and (before.channel != after.channel):
        alert_channel = bot.get_channel(CHANNEL_ID) # alertChannnel
        print("alert_channel>> ", alert_channel)
        if before.channel is None:
            if after.channel.members is not None:
                role = discord.utils.get(member.guild.roles, name="notify")
                msg = f'{role.mention} {member.display_name} が {after.channel.name} に参加しました。'
                await alert_channel.send(msg)


bot.run(DISCORD_TOKEN)
